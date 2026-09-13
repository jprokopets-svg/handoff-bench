"""import re

def run_program(src, inputs=None):
    lines = [line.strip() for line in src.strip().split('\n')]
    lines = [line for line in lines if line]
    
    jump_map = build_jump_map(lines)
    
    env = {}
    output = []
    inputs = list(inputs) if inputs is not None else []
    input_idx = 0
    
    pc = 0
    while pc < len(lines):
        line = lines[pc]
        
        if_match = re.match(r'if (.+?) {', line)
        while_match = re.match(r'while (.+?) {', line)
        else_match = re.match(r'} else {', line)
        assign_match = re.match(r'(\w+) = (.+)', line)
        print_match = re.match(r'print\((.+)\)', line)
        input_match = re.match(r'(\w+) = input\(\)', line)

        if line == '}':
            if pc in jump_map: # It's a while loop's end
                pc = jump_map[pc]
                continue
            # else it's an if/else block's end, just continue
        elif if_match:
            cond_str = if_match.group(1)
            val = evaluate(cond_str, env)
            if val == 0:
                pc = jump_map[pc] # Jump to '}' or '} else {'
        elif while_match:
            cond_str = while_match.group(1)
            val = evaluate(cond_str, env)
            if val == 0:
                pc = jump_map[pc] # Jump to '}'
        elif else_match:
            pc = jump_map[pc] # Jump to final '}' of else block
        elif line == '}':
            pass # Handled by jump map logic
        elif assign_match:
            var, expr = assign_match.groups()
            if expr == 'input()':
                 if input_idx >= len(inputs):
                    raise ValueError("Not enough inputs")
                 env[var] = inputs[input_idx]
                 input_idx += 1
            else:
                env[var] = evaluate(expr, env)
        elif print_match:
            expr = print_match.group(1)
            val = evaluate(expr, env)
            output.append(str(val) + '\n')
        elif input_match:
            var = input_match.group(1)
            if not inputs:
                raise ValueError("input() called with no inputs left")
            env[var] = inputs.pop(0)
        else:
            raise ValueError(f"Syntax error on line: {line}")
        
        pc += 1
        
    return "".join(output)

def build_jump_map(lines):
    jump_map = {}
    stack = []
    for i, line in enumerate(lines):
        if line.endswith('{'):
            stack.append(i)
        elif line == '}':
            if not stack:
                raise ValueError("Stray '}'")
            start = stack.pop()
            if lines[start].startswith('while'):
                jump_map[i] = start # Jump back to the while
                jump_map[start] = i # Jump forward if cond is false
            else: # if block
                jump_map[start] = i # Jump forward if cond is false
        elif line == '} else {':
            if not stack:
                raise ValueError("Stray '} else {'")
            start_if = stack.pop()
            if not lines[start_if].startswith('if'):
                 raise ValueError("else without if")
            jump_map[start_if] = i # if false, jump to else
            stack.append(i) # for the '}' of the else block
            
    if stack:
        raise ValueError("Unbalanced braces")
    return jump_map


def evaluate(expr, env):
    tokens = tokenize(expr)
    values = []
    ops = []

    def precedence(op):
        if op in ('*', '/', '%'): return 3
        if op in ('+', '-'): return 2
        if op in ('==', '!=', '<', '<=', '>', '>='): return 1
        return 0

    def apply_op():
        op = ops.pop()
        right = values.pop()
        left = values.pop()
        if op == '+': values.append(left + right)
        elif op == '-': values.append(left - right)
        elif op == '*': values.append(left * right)
        elif op == '/':
            if right == 0: raise ValueError("Division by zero")
            values.append(int(left / right))
        elif op == '%':
            if right == 0: raise ValueError("Modulo by zero")
            values.append(left % right)
        elif op == '==': values.append(int(left == right))
        elif op == '!=': values.append(int(left != right))
        elif op == '<': values.append(int(left < right))
        elif op == '<=': values.append(int(left <= right))
        elif op == '>': values.append(int(left > right))
        elif op == '>=': values.append(int(left >= right))

    i = 0
    while i < len(tokens):
        token = tokens[i]
        if isinstance(token, int):
            values.append(token)
        elif isinstance(token, str) and token.isidentifier():
            if token not in env:
                raise ValueError(f"Undefined variable: {token}")
            values.append(env[token])
        elif token == '(':
            ops.append(token)
        elif token == ')':
            while ops and ops[-1] != '(':
                apply_op()
            if not ops or ops[-1] != '(':
                raise ValueError("Mismatched parentheses")
            ops.pop()
        else: # Operator
            while ops and ops[-1] != '(' and precedence(ops[-1]) >= precedence(token):
                apply_op()
            ops.append(token)
        i += 1

    while ops:
        if ops[-1] == '(': raise ValueError("Mismatched parentheses")
        apply_op()
    
    if len(values) != 1 or ops:
        raise ValueError("Syntax error in expression")

    return values[0]

def tokenize(expr):
    token_regex = r'\s*(\d+|[a-zA-Z_]\w*|==|!=|<=|>=|[-+*/%()<>{}=])\s*'
    tokens = re.findall(token_regex, expr)
    reconstructed = "".join(tokens)
    if reconstructed != expr.replace(" ", ""):
        raise ValueError(f"Syntax error in expression: {expr}")
    
    processed_tokens = []
    for token in tokens:
        if token.isdigit():
            processed_tokens.append(int(token))
        else:
            processed_tokens.append(token)
    return processed_tokens
""