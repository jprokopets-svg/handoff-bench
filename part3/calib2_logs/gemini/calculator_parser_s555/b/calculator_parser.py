import re

def evaluate(expression: str) -> float:
    tokens = tokenize(expression)
    postfix_tokens = shunting_yard(tokens)
    return evaluate_postfix(postfix_tokens)

def tokenize(expression: str) -> list:
    if not expression.strip():
        raise ValueError("Empty expression")
    
    # Regular expression to match numbers, operators, and parentheses
    # Numbers: integers, decimals (e.g., 3.5, 0.5, .5, 3.)
    # Operators: **, *, /, %, +, -
    # Parentheses: (, )
    token_pattern = re.compile(r'(\d+\.?\d*|\.?\d+|\*\*|[+\-*/%()])')
    
    tokens = []
    last_token_type = 'START' # 'START', 'NUMBER', 'OPERATOR', 'PAREN_OPEN', 'PAREN_CLOSE'
    
    for match in token_pattern.finditer(expression):
        token = match.group(0)
        
        if token.isspace():
            continue
            
        if re.fullmatch(r'\d+\.?\d*|\.?\d+', token):
            tokens.append(float(token))
            last_token_type = 'NUMBER'
        elif token in ['+', '-']:
            # Determine if it's a unary or binary operator
            if last_token_type in ['START', 'OPERATOR', 'PAREN_OPEN']:
                if token == '-':
                    tokens.append('UNARY_MINUS')
                else:
                    tokens.append('UNARY_PLUS')
            else:
                tokens.append(token)
            last_token_type = 'OPERATOR'
        elif token in ['*', '/', '%', '**']:
            tokens.append(token)
            last_token_type = 'OPERATOR'
        elif token == '(':
            tokens.append(token)
            last_token_type = 'PAREN_OPEN'
        elif token == ')':
            tokens.append(token)
            last_token_type = 'PAREN_CLOSE'
        else:
            raise ValueError(f"Invalid token: {token}")
            
    if not tokens:
        raise ValueError("Empty expression")
    
    return tokens

def shunting_yard(tokens: list) -> list:
    output_queue = []
    operator_stack = []
    
    precedence = {
        '**': 6, # Highest precedence
        'UNARY_PLUS': 5,
        'UNARY_MINUS': 5,
        '*': 4,
        '/': 4,
        '%': 4,
        '+': 3,
        '-': 3,
    }
    
    associativity = {
        '**': 'right',
        '*': 'left',
        '/': 'left',
        '%': 'left',
        '+': 'left',
        '-': 'left',
        'UNARY_PLUS': 'right',
        'UNARY_MINUS': 'right',
    }
    
    for token in tokens:
        if isinstance(token, float):
            output_queue.append(token)
        elif token in precedence:
            while (operator_stack and operator_stack[-1] != '(' and
                   ((associativity.get(token) == 'left' and precedence.get(operator_stack[-1]) >= precedence[token]) or
                    (associativity.get(token) == 'right' and precedence.get(operator_stack[-1]) > precedence[token]))):
                output_queue.append(operator_stack.pop())
            operator_stack.append(token)
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            while operator_stack and operator_stack[-1] != '(':
                output_queue.append(operator_stack.pop())
            if not operator_stack:
                raise ValueError("Mismatched parentheses")
            operator_stack.pop() # Pop '('
        else:
            raise ValueError(f"Unknown token during shunting yard: {token}")
            
    while operator_stack:
        if operator_stack[-1] == '(':
            raise ValueError("Mismatched parentheses")
        output_queue.append(operator_stack.pop())
        
    return output_queue

def evaluate_postfix(tokens: list) -> float:
    operand_stack = []
    
    for token in tokens:
        if isinstance(token, float):
            operand_stack.append(token)
        else:
            if token == 'UNARY_MINUS':
                if not operand_stack:
                    raise ValueError("Invalid expression: unary minus needs an operand")
                operand = operand_stack.pop()
                operand_stack.append(-operand)
            elif token == 'UNARY_PLUS':
                if not operand_stack:
                    raise ValueError("Invalid expression: unary plus needs an operand")
                operand = operand_stack.pop()
                operand_stack.append(operand)
            else:
                if len(operand_stack) < 2:
                    raise ValueError("Invalid expression: operator needs two operands")
                operand2 = operand_stack.pop()
                operand1 = operand_stack.pop()
                
                if token == '+':
                    operand_stack.append(operand1 + operand2)
                elif token == '-':
                    operand_stack.append(operand1 - operand2)
                elif token == '*':
                    operand_stack.append(operand1 * operand2)
                elif token == '/':
                    if operand2 == 0:
                        raise ValueError("Division by zero")
                    operand_stack.append(operand1 / operand2)
                elif token == '%':
                    if operand2 == 0:
                        raise ValueError("Modulo by zero")
                    operand_stack.append(operand1 % operand2)
                elif token == '**':
                    operand_stack.append(operand1 ** operand2)
                else:
                    raise ValueError(f"Unknown operator during postfix evaluation: {token}")
                    
    if len(operand_stack) != 1:
        raise ValueError("Invalid expression: too many operands or operators")
        
    return operand_stack[0]
