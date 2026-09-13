
import re

def run_program(src, inputs=None):
    lines = [line.strip() for line in src.split('\\n') if line.strip()]
    inputs = list(inputs) if inputs is not None else []
    env = {}
    output = []
    pc = 0
    
    # Pre-computation for control flow
    brace_map = {}
    brace_stack = []
    for i, line in enumerate(lines):
        if '{' in line:
            brace_stack.append(i)
        if line.startswith('}'):
            if not brace_stack:
                raise ValueError("Stray '}'")
            start = brace_stack.pop()
            brace_map[start] = i
            brace_map[i] = start
    if brace_stack:
        raise ValueError("Unbalanced braces")

    # Expression evaluation logic
    prec = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2, '==': 0, '!=': 0, '<': 0, '<=': 0, '>': 0, '>=': 0}
    ops_fn = {
        '+': lambda a, b: a + b, '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: int(a / b) if b != 0 else (_ for _ in ()).throw(ValueError("Division by zero")),
        '%': lambda a, b: a % b if b != 0 else (_ for _ in ()).throw(ValueError("Modulo by zero")),
        '==': lambda a, b: int(a == b), '!=': lambda a, b: int(a != b),
        '<': lambda a, b: int(a < b), '<=': lambda a, b: int(a <= b),
        '>': lambda a, b: int(a > b), '>=': lambda a, b: int(a >= b),
    }

    def evaluate_expr(tokens, local_env):
        if not tokens:
            raise ValueError("Empty expression")

        values = []
        ops = []

        def apply_op():
            op = ops.pop()
            right = values.pop()
            left = values.pop()
            values.append(ops_fn[op](left, right))

        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token.isdigit() or (token.startswith('-') and token[1:].isdigit()):
                values.append(int(token))
            elif token.isalpha():
                if token not in local_env:
                    raise ValueError(f"Undefined variable: {token}")
                values.append(local_env[token])
            elif token == '(':
                ops.append(token)
            elif token == ')':
                while ops and ops[-1] != '(':
                    apply_op()
                if not ops or ops[-1] != '(':
                    raise ValueError("Unbalanced parentheses")
                ops.pop()
            elif token in ops_fn:
                while ops and ops[-1] != '(' and prec.get(ops[-1], -1) >= prec.get(token, -1):
                    apply_op()
                ops.append(token)
            else:
                raise ValueError(f"Unexpected token: {token}")
            i += 1
        
        while ops:
            if ops[-1] == '(':
                raise ValueError("Unbalanced parentheses")
            apply_op()

        if len(values) != 1 or ops:
            raise ValueError("Syntax error in expression")
        return values[0]

    def tokenize(expr_str):
        # Pad operators with spaces to ensure split captures them
        expr_str = expr_str.replace('(', ' ( ').replace(')', ' ) ')
        for op in ['==', '!=', '<=', '>=', '<', '>', '+', '-', '*', '/', '%']:
            expr_str = expr_str.replace(op, f' {op} ')
        return expr_str.split()

    # Main execution loop
    exec_stack = [True] # Stack to control execution of blocks
    
    while pc < len(lines):
        line = lines[pc]
        
        if not exec_stack[-1]:
            if '{' in line:
                pc = brace_map[pc]
            elif line.startswith('}') and pc + 1 < len(lines) and lines[pc+1] == 'else {':
                 # If we are skipping an if-block, we might need to execute the else
                 if exec_stack[-2]: # Check the condition that started the parent block
                     exec_stack[-1] = True
                     pc += 1 # Move to 'else {'
                 else:
                     pc = brace_map[pc+1] # Skip the else block too
            elif line.startswith('}'):
                # Finished skipping a block
                exec_stack.pop()
            pc += 1
            continue

        if_match = re.match(r'if (.+?) {', line)
        while_match = re.match(r'while (.+?) {', line)
        assign_match = re.match(r'(\w+)\s*=\s*(.+)', line)
        print_match = re.match(r'print\((.+)\)', line)

        if if_match:
            cond_str = if_match.group(1)
            cond_val = evaluate_expr(tokenize(cond_str), env)
            exec_stack.append(bool(cond_val))
            if not cond_val:
                pc = brace_map[pc] # Jump to '}'
        elif while_match:
            cond_str = while_match.group(1)
            cond_val = evaluate_expr(tokenize(cond_str), env)
            exec_stack.append(bool(cond_val))
            if not cond_val:
                pc = brace_map[pc] # Jump to '}'
        elif line == '}':
            start_block_pc = brace_map[pc]
            start_line = lines[start_block_pc]
            if start_line.startswith('while'):
                pc = start_block_pc - 1 # Loop back, pc will be incremented to the while line
                exec_stack.pop()
            elif start_line.startswith('if'):
                exec_stack.pop() # End of if block
        elif line == '} else {':
            start_if_pc = brace_map[pc]
            # This else block should be skipped because the if block was executed
            pc = brace_map[pc] # Jump to the '}' of the else block
            exec_stack.append(False) # Push a false to the stack to skip the else block
        elif print_match:
            expr_str = print_match.group(1)
            val = evaluate_expr(tokenize(expr_str), env)
            output.append(str(val) + '\\n')
        elif assign_match:
            var_name = assign_match.group(1)
            expr_str = assign_match.group(2)
            if expr_str == 'input()':
                if not inputs:
                    raise ValueError("Input exhausted")
                env[var_name] = inputs.pop(0)
            else:
                env[var_name] = evaluate_expr(tokenize(expr_str), env)
        else:
            raise ValueError(f"Syntax error on line: {line}")
        
        pc += 1

    return "".join(output)
