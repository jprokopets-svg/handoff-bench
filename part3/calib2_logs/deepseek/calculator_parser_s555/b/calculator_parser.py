def evaluate(expr: str) -> float:
    # Tokenization
    tokens = []
    i = 0
    n = len(expr)
    
    while i < n:
        ch = expr[i]
        if ch.isspace():
            i += 1
            continue
        # Number: digit sequence with optional decimal point
        if ch.isdigit() or ch == '.':
            # Validate: digit must precede decimal point
            start = i
            has_digit = False
            has_dot = False
            while i < n and (expr[i].isdigit() or expr[i] == '.'):
                if expr[i] == '.':
                    if has_dot:
                        # Multiple dots invalid
                        raise ValueError("Invalid number")
                    has_dot = True
                else:
                    has_digit = True
                i += 1
            # Check digit before decimal
            if has_dot and not has_digit:
                raise ValueError("Invalid number: digit must precede decimal point")
            if not has_digit:
                raise ValueError("Invalid number")
            num_str = expr[start:i]
            tokens.append(float(num_str))
            continue
        # Operators and parentheses
        if ch in '+-*/%()':
            tokens.append(ch)
            i += 1
            continue
        # Exponentiation operator **
        if ch == '*':
            if i + 1 < n and expr[i + 1] == '*':
                tokens.append('**')
                i += 2
                continue
            tokens.append('*')
            i += 1
            continue
        # Invalid character
        raise ValueError(f"Invalid token '{ch}'")
    
    # Convert infix to RPN using shunting-yard
    output = []
    stack = []
    
    # Helper to determine if token is operator
    def is_operator(tok):
        return tok in ('+', '-', '*', '/', '%', '**')
    
    # Precedence: higher number = higher precedence
    precedence = {
        '**': 4,
        'u+': 3,  # unary plus
        'u-': 3,  # unary minus
        '*': 2,
        '/': 2,
        '%': 2,
        '+': 1,
        '-': 1,
    }
    
    # Determine if '-' or '+' is unary
    def handle_unary(i):
        # Check if token at position i is a unary + or -
        if tokens[i] not in ('+', '-'):
            return tokens[i]
        # Unary if:
        # 1. First token
        if i == 0:
            return 'u' + tokens[i]
        # 2. Previous token is '(' or operator (including **)
        prev = tokens[i - 1]
        if prev == '(' or (is_operator(prev) and prev != ')'):
            return 'u' + tokens[i]
        # 3. Previous token is unary operator (should not happen due to detection)
        return tokens[i]
    
    # Process tokens
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        # Handle unary +/-
        if tok in ('+', '-'):
            tok = handle_unary(i)
        
        if isinstance(tok, float):
            output.append(tok)
        elif tok == '(':
            stack.append(tok)
        elif tok == ')':
            # Pop until '('
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if not stack or stack[-1] != '(':
                raise ValueError("Mismatched parentheses")
            stack.pop()  # discard '('
        elif is_operator(tok) or tok in ('u+', 'u-'):
            # Right-associative: **
            # Left-associative: others
            while stack and stack[-1] != '(':
                top = stack[-1]
                if (precedence.get(top, 0) > precedence.get(tok, 0) or
                    (precedence.get(top, 0) == precedence.get(tok, 0) and
                     tok != '**')):  # left-associative except **
                    output.append(stack.pop())
                else:
                    break
            stack.append(tok)
        i += 1
    
    # Pop remaining operators
    while stack:
        if stack[-1] == '(':
            raise ValueError("Mismatched parentheses")
        output.append(stack.pop())
    
    # Evaluate RPN
    eval_stack = []
    for token in output:
        if isinstance(token, float):
            eval_stack.append(token)
        elif token in ('u+', 'u-'):
            if len(eval_stack) < 1:
                raise ValueError("Invalid expression")
            a = eval_stack.pop()
            if token == 'u+':
                eval_stack.append(a)
            else:  # 'u-'
                eval_stack.append(-a)
        else:
            # Binary operator
            if len(eval_stack) < 2:
                raise ValueError("Invalid expression")
            b = eval_stack.pop()
            a = eval_stack.pop()
            if token == '+':
                eval_stack.append(a + b)
            elif token == '-':
                eval_stack.append(a - b)
            elif token == '*':
                eval_stack.append(a * b)
            elif token == '/':
                if b == 0:
                    raise ValueError("Division by zero")
                eval_stack.append(a / b)
            elif token == '%':
                if b == 0:
                    raise ValueError("Modulo by zero")
                # Python's % with floats
                eval_stack.append(a % b)
            elif token == '**':
                eval_stack.append(a ** b)
            else:
                raise ValueError(f"Unknown operator {token}")
    
    if len(eval_stack) != 1:
        raise ValueError("Invalid expression")
    
    return float(eval_stack[0])