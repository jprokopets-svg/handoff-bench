
import re

def run_program(src, inputs=None):
    lines = [line.strip() for line in src.split('\n') if line.strip()]
    inputs = list(inputs) if inputs is not None else []
    env = {}
    output = []
    pc = 0
    
    # Pre-computation for control flow
    jump_map = {}
    brace_stack = []
    for i, line in enumerate(lines):
        if '{' in line:
            brace_stack.append(i)
        if line.startswith('}'):
            if not brace_stack:
                raise ValueError("Stray '}'")
            start = brace_stack.pop()
            
            # Handle '} else {'
            if line == '}' and i + 1 < len(lines) and lines[i+1] == '} else {':
                jump_map[start] = i + 1 
                # The else block now needs a closing brace
                brace_stack.append(i + 1)
            else:
                jump_map[start] = i
                jump_map[i] = start

    if brace_stack:
        raise ValueError("Unbalanced braces")

    # Expression evaluation logic (Shunting-yard)
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
            try:
                op = ops.pop()
                right = values.pop()
                left = values.pop()
                values.append(ops_fn[op](left, right))
            except IndexError:
                raise ValueError("Syntax error in expression")

        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token.isdigit() or (token.startswith('-') and token[1:].isdigit() and (i == 0 or tokens[i-1] in prec or tokens[i-1] == '(')):
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
                ops.pop() # Pop '('
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
        expr_str = expr_str.replace('(', ' ( ').replace(')', ' ) ')
        # Use a regex to handle operators and avoid splitting numbers
        tokens = re.findall(r'-?\d+|\w+|[\+\-\*\/%<>=!]=?|\(|\)', expr_str)
        return tokens

    # Main execution loop
    while pc < len(lines):
        line = lines[pc]
        
        if_match = re.match(r'if (.+?) {', line)
        while_match = re.match(r'while (.+?) {', line)
        assign_match = re.match(r'(\w+)\s*=\s*(.+)', line)
        print_match = re.match(r'print\((.+)\)', line)

        if if_match:
            cond_str = if_match.group(1)
            cond_val = evaluate_expr(tokenize(cond_str), env)
            if not cond_val:
                pc = jump_map[pc] # Jump to '}' or '} else {'
        elif while_match:
            cond_str = while_match.group(1)
            cond_val = evaluate_expr(tokenize(cond_str), env)
            if not cond_val:
                pc = jump_map[pc] # Jump to '}'
        elif line == '}':
            start_block_pc = jump_map[pc]
            start_line = lines[start_block_pc]
            if start_line.startswith('while'):
                pc = start_block_pc - 1 # Loop back
            # If it's an if block, we might need to skip a following else
            elif start_line.startswith('if') and pc + 1 < len(lines) and lines[pc+1] == '} else {':
                pc = jump_map[pc + 1] # Skip the else block
        elif line == '} else {':
            # This line is only reached if the 'if' was false.
            # The end of this block is handled by the '}' case.
            pass
        elif print_match:
            expr_str = print_match.group(1)
            val = evaluate_expr(tokenize(expr_str), env)
            output.append(str(val) + '\n')
        elif assign_match:
            var_name, expr_str = assign_match.groups()
            if var_name in ('if', 'while', 'print', 'else'):
                 raise ValueError(f"Cannot assign to keyword: {var_name}")
            if expr_str == 'input()':
                if not inputs:
                    raise ValueError("Input exhausted")
                env[var_name] = inputs.pop(0)
            else:
                env[var_name] = evaluate_expr(tokenize(expr_str), env)
        elif line.strip() != '':
             raise ValueError(f"Syntax error on line: {line}")
        
        pc += 1

    return "".join(output)
