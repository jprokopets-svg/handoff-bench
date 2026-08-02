import re

def evaluate(expression: str) -> float:
    # Tokenization
    # This regex handles numbers (integers and floats), operators, and parentheses.
    # It also handles whitespace.
    token_pattern = re.compile(r'(\\d+\\.?\\d*|\\.\\d+|\\*\\*|[+\-*/%()]|\\s+)')
    
    # Split the expression into raw tokens, including whitespace
    raw_tokens = [t for t in token_pattern.findall(expression) if t.strip()]
    
    tokens = []
    # Process raw tokens to handle unary operators and filter out whitespace
    i = 0
    while i < len(raw_tokens):
        token = raw_tokens[i]
        if token.isspace():
            i += 1
            continue

        if token == '-' and (i == 0 or raw_tokens[i-1] in '(*+/-^%' or raw_tokens[i-1].isspace()):
            tokens.append('U-')
        elif token == '+' and (i == 0 or raw_tokens[i-1] in '(*+/-^%' or raw_tokens[i-1].isspace()):
            tokens.append('U+')
        else:
            tokens.append(token)
        i += 1

    if not tokens:
        raise ValueError("Empty expression")

    # Shunting-Yard Algorithm
    output_queue = []
    operator_stack = []
    
    precedence = {
        'U-': 5, 'U+': 5,
        '**': 4,
        '*': 3, '/': 3, '%': 3,
        '+': 2, '-': 2,
    }
    
    associativity = {
        '**': 'right',
        '*': 'left', '/': 'left', '%': 'left',
        '+': 'left', '-': 'left',
        'U-': 'right', 'U+': 'right' # Unary operators are typically right-associative
    }

    i = 0
    while i < len(tokens):
        token = tokens[i]
        if re.match(r'\\d+\\.?\\d*|\\.\\d+', token):  # Number
            output_queue.append(float(token))
        elif token in precedence:  # Operator
            while (operator_stack and operator_stack[-1] != '(' and
                   (precedence.get(operator_stack[-1], 0) > precedence[token] or
                    (precedence.get(operator_stack[-1], 0) == precedence[token] and associativity.get(token) == 'left'))):
                output_queue.append(operator_stack.pop())
            operator_stack.append(token)
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            while operator_stack and operator_stack[-1] != '(':
                output_queue.append(operator_stack.pop())
            if not operator_stack:
                raise ValueError("Mismatched parentheses")
            operator_stack.pop()  # Pop '('
        else:
            raise ValueError(f"Invalid token: {token}")
        i += 1

    while operator_stack:
        if operator_stack[-1] == '(':
            raise ValueError("Mismatched parentheses")
        output_queue.append(operator_stack.pop())

    # RPN Evaluation
    operand_stack = []
    for token in output_queue:
        if isinstance(token, float):
            operand_stack.append(token)
        else:  # Operator
            if token in ('U-', 'U+'):
                if len(operand_stack) < 1:
                    raise ValueError("Invalid expression: unary operator with insufficient operands")
                operand = operand_stack.pop()
                if token == 'U-':
                    operand_stack.append(-operand)
                elif token == 'U+':
                    operand_stack.append(operand)
            else:
                if len(operand_stack) < 2:
                    raise ValueError("Invalid expression: binary operator with insufficient operands")
                right = operand_stack.pop()
                left = operand_stack.pop()
                if token == '+':
                    operand_stack.append(left + right)
                elif token == '-':
                    operand_stack.append(left - right)
                elif token == '*':
                    operand_stack.append(left * right)
                elif token == '/':
                    if right == 0:
                        raise ValueError("Division by zero")
                    operand_stack.append(left / right)
                elif token == '%':
                    if right == 0:
                        raise ValueError("Modulo by zero")
                    operand_stack.append(left % right)
                elif token == '**':
                    operand_stack.append(left ** right)
    
    if len(operand_stack) != 1:
        raise ValueError("Invalid expression")

    return operand_stack[0]
