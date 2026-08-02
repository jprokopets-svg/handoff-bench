def evaluate(expr: str) -> float:
    # Tokenize the expression
    tokens = []
    i = 0
    n = len(expr)
    
    while i < n:
        ch = expr[i]
        
        # Skip whitespace
        if ch.isspace():
            i += 1
            continue
            
        # Number: integer or decimal
        if ch.isdigit() or (ch == '.' and i + 1 < n and expr[i+1].isdigit()):
            # Handle number
            start = i
            # Check for leading digit before decimal point
            if ch == '.':
                # Must have digit before decimal point according to spec
                # But we're already checking that expr[i+1].isdigit()
                # However spec says "a digit must precede the decimal point"
                # So .5 is invalid, but 0.5 is valid
                # Actually reading spec: "Numbers may be integers or decimals (a digit must precede the decimal point: 3.5, 0.5)"
                # So .5 is invalid, 0.5 is valid
                # We'll handle this during parsing
                pass
            
            # Parse number
            has_digit_before_decimal = False
            if ch.isdigit():
                has_digit_before_decimal = True
                
            while i < n and (expr[i].isdigit() or expr[i] == '.'):
                if expr[i].isdigit():
                    has_digit_before_decimal = True
                i += 1
                
            # Check if we have a valid number
            num_str = expr[start:i]
            # Check for multiple decimal points
            if num_str.count('.') > 1:
                raise ValueError("Invalid number")
            # Check that we have a digit before decimal point if there's a decimal point
            if '.' in num_str and not has_digit_before_decimal:
                raise ValueError("Invalid number: digit must precede decimal point")
                
            tokens.append(('NUM', float(num_str)))
            continue
            
        # Operators and parentheses
        if ch in '+-*/%()':
            # Check for unary + or -
            if ch in '+-':
                # Check if it's unary:
                # 1. At start of expression
                # 2. After '('
                # 3. After another operator
                if not tokens:
                    # Start of expression
                    tokens.append(('UNARY', ch))
                elif tokens[-1][0] in ('OP', 'UNARY', '('):
                    # After operator or '('
                    tokens.append(('UNARY', ch))
                else:
                    # Binary operator
                    tokens.append(('OP', ch))
            elif ch == '*':
                # Check for ** operator
                if i + 1 < n and expr[i+1] == '*':
                    tokens.append(('OP', '**'))
                    i += 1
                else:
                    tokens.append(('OP', '*'))
            else:
                tokens.append(('PAREN' if ch in '()' else 'OP', ch))
            i += 1
            continue
            
        # Invalid character
        raise ValueError(f"Invalid token: {ch}")
    
    # Check for empty expression
    if not tokens:
        raise ValueError("Empty expression")
    
    # Check for trailing operator
    if tokens[-1][0] in ('OP', 'UNARY'):
        raise ValueError("Trailing operator")
    
    # Convert to RPN using shunting-yard algorithm
    output = []
    op_stack = []
    
    # Operator precedence and associativity
    precedence = {
        '**': 4,
        'u+': 3,  # Unary plus
        'u-': 3,  # Unary minus
        '*': 2,
        '/': 2,
        '%': 2,
        '+': 1,
        '-': 1,
    }
    
    # For checking adjacency of operands
    last_was_operand = False
    
    for token_type, token_value in tokens:
        if token_type == 'NUM':
            output.append(('NUM', token_value))
            last_was_operand = True
        elif token_type == 'UNARY':
            # Convert unary to special operator tokens
            op = 'u+' if token_value == '+' else 'u-'
            op_stack.append(('OP', op))
            last_was_operand = False
        elif token_type == 'OP':
            # Check for two adjacent operands without operator
            if last_was_operand and token_value in '+-*/%**':
                # This is okay - we have an operator between operands
                pass
            elif not last_was_operand and token_value in '+-*/%**':
                # Operator without left operand - should have been caught as unary
                pass
                
            # Handle operator precedence
            while (op_stack and op_stack[-1][0] == 'OP' and
                   op_stack[-1][1] != '(' and
                   (precedence[op_stack[-1][1]] > precedence[token_value] or
                    (precedence[op_stack[-1][1]] == precedence[token_value] and 
                     token_value != '**'))):  # ** is right-associative, others left
                output.append(op_stack.pop())
            
            op_stack.append(('OP', token_value))
            last_was_operand = False
        elif token_value == '(':
            op_stack.append(('PAREN', '('))
            last_was_operand = False
        elif token_value == ')':
            # Pop until matching '('
            found = False
            while op_stack:
                top_type, top_value = op_stack.pop()
                if top_type == 'PAREN' and top_value == '(':
                    found = True
                    break
                output.append((top_type, top_value))
            
            if not found:
                raise ValueError("Unbalanced parentheses")
            
            # Check if there's a unary operator before '('
            if op_stack and op_stack[-1][0] == 'OP' and op_stack[-1][1] in ('u+', 'u-'):
                output.append(op_stack.pop())
            
            last_was_operand = True
    
    # Pop remaining operators
    while op_stack:
        top_type, top_value = op_stack.pop()
        if top_type == 'PAREN':
            raise ValueError("Unbalanced parentheses")
        output.append((top_type, top_value))
    
    # Evaluate RPN
    stack = []
    
    for token_type, token_value in output:
        if token_type == 'NUM':
            stack.append(token_value)
        else:
            # Operator
            if token_value in ('u+', 'u-'):
                # Unary operator
                if not stack:
                    raise ValueError("Invalid expression")
                a = stack.pop()
                if token_value == 'u+':
                    stack.append(+a)
                else:  # 'u-'
                    stack.append(-a)
            else:
                # Binary operator
                if len(stack) < 2:
                    raise ValueError("Invalid expression")
                b = stack.pop()
                a = stack.pop()
                
                if token_value == '+':
                    stack.append(a + b)
                elif token_value == '-':
                    stack.append(a - b)
                elif token_value == '*':
                    stack.append(a * b)
                elif token_value == '/':
                    if b == 0:
                        raise ValueError("Division by zero")
                    stack.append(a / b)
                elif token_value == '%':
                    if b == 0:
                        raise ValueError("Modulo by zero")
                    stack.append(a % b)
                elif token_value == '**':
                    stack.append(a ** b)
    
    if len(stack) != 1:
        raise ValueError("Invalid expression")
    
    return stack[0]