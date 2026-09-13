
import re

def evaluate(expression):
    if not isinstance(expression, str):
        raise TypeError("Expression must be a string")

    # Precedence and associativity
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2, '**': 4, 'u-': 3, 'u+': 3}
    associativity = {'+': 'L', '-': 'L', '*': 'L', '/': 'L', '%': 'L', '**': 'R', 'u-': 'R', 'u+': 'R'}

    def apply_operator(operators, values):
        operator = operators.pop()
        if operator.startswith('u'): # Unary operators
            if not values:
                raise ValueError("Invalid expression: Not enough operands for unary operator")
            right = values.pop()
            if operator == 'u-':
                values.append(-right)
            # Unary plus has no effect, so we do nothing
        else: # Binary operators
            if len(values) < 2:
                raise ValueError("Invalid expression: Not enough operands for binary operator")
            right = values.pop()
            left = values.pop()
            if operator == '+':
                values.append(left + right)
            elif operator == '-':
                values.append(left - right)
            elif operator == '*':
                values.append(left * right)
            elif operator == '/':
                if right == 0:
                    raise ValueError("Division by zero")
                values.append(left / right)
            elif operator == '%':
                if right == 0:
                    raise ValueError("Modulo by zero")
                # Python's % behaves like math mod, which is what's needed.
                # a % n = a - n * floor(a/n)
                values.append(left % right)
            elif operator == '**':
                values.append(left ** right)

    tokens = re.findall(r'\d+(?:\.\d*)?|\.\d+|\*\*|[-+*/%()]|\S+', expression)
    
    # Check for invalid tokens
    valid_tokens = re.compile(r'^(\d+(?:\.\d*)?|\.\d+|\*\*|[-+*/%()])$')
    for t in tokens:
        if not valid_tokens.match(t):
            raise ValueError(f"Invalid token: {t}")

    values = []
    operators = []
    last_token_was_op_or_lparen = True

    for i, token in enumerate(tokens):
        if token.replace('.', '', 1).isdigit():
            if not last_token_was_op_or_lparen:
                 raise ValueError("Two adjacent operands without an operator")
            values.append(float(token))
            last_token_was_op_or_lparen = False
        elif token == '(':
            if not last_token_was_op_or_lparen and i > 0:
                raise ValueError("Operand followed by opening parenthesis")
            operators.append(token)
            last_token_was_op_or_lparen = True
        elif token == ')':
            if last_token_was_op_or_lparen and operators[-1] != '(':
                raise ValueError("Empty parentheses or trailing operator inside parentheses")
            while operators and operators[-1] != '(':
                apply_operator(operators, values)
            if not operators or operators.pop() != '(':
                raise ValueError("Mismatched parentheses")
            last_token_was_op_or_lparen = False
        else: # Operator
            if last_token_was_op_or_lparen: # Unary
                if token == '-':
                    op = 'u-'
                elif token == '+':
                    op = 'u+'
                else: # *, /, %, ** cannot be unary
                    raise ValueError(f"Invalid unary operator: {token}")
            else: # Binary
                op = token

            while (operators and operators[-1] != '(' and
                   (precedence.get(operators[-1], 0) > precedence.get(op, 0) or
                    (precedence.get(operators[-1], 0) == precedence.get(op, 0) and associativity.get(op) == 'L'))):
                apply_operator(operators, values)
            operators.append(op)
            last_token_was_op_or_lparen = True
    
    if last_token_was_op_or_lparen and tokens:
        raise ValueError("Trailing operator")
    if not tokens and not values:
        raise ValueError("Empty expression")

    while operators:
        if operators[-1] == '(':
            raise ValueError("Mismatched parentheses")
        apply_operator(operators, values)

    if len(values) != 1:
        raise ValueError("Invalid expression")
        
    return values[0]
