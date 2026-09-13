import re
from typing import List, Union

def evaluate(expr: str) -> float:
    """Evaluate an infix arithmetic expression and return the numeric result as a float."""
    if not expr or expr.isspace():
        raise ValueError("Empty expression")
    
    # Tokenize the expression
    tokens = tokenize(expr)
    if not tokens:
        raise ValueError("Empty expression")
    
    # Convert infix to RPN using shunting-yard algorithm
    rpn = shunting_yard(tokens)
    
    # Evaluate RPN
    return evaluate_rpn(rpn)


def tokenize(expr: str) -> List[str]:
    """Tokenize expression into numbers, operators, and parentheses."""
    # Remove whitespace
    expr = expr.replace(' ', '')
    
    # Regular expression to match numbers, operators, and parentheses
    # Numbers: integer or decimal (must have digit before decimal)
    # Operators: **, *, /, %, +, -
    # Parentheses: (, )
    token_pattern = r"""
        \d+(?:\.\d+)?    # Numbers: integer or decimal
        |\*\*            # Exponentiation operator
        |[*/%+\-()]      # Other operators and parentheses
    """
    
    tokens = re.findall(token_pattern, expr, re.VERBOSE)
    
    # Check if we matched the entire expression
    joined = ''.join(tokens)
    if joined != expr:
        raise ValueError("Invalid token in expression")
    
    return tokens


def shunting_yard(tokens: List[str]) -> List[str]:
    """Convert infix tokens to RPN using shunting-yard algorithm."""
    output = []
    stack = []
    
    # Helper to get precedence of operator
    def precedence(op: str) -> int:
        if op == '**':
            return 4
        elif op in ('u+', 'u-'):  # Unary operators
            return 3
        elif op in ('*', '/', '%'):
            return 2
        elif op in ('+', '-'):
            return 1
        return 0
    
    # Helper to check if token is an operator
    def is_operator(token: str) -> bool:
        return token in ('**', '*', '/', '%', '+', '-', 'u+', 'u-')
    
    # Helper to check if token is a unary operator
    def is_unary(token: str, prev_token: str) -> bool:
        """Determine if + or - is unary based on context."""
        if token not in ('+', '-'):
            return False
        
        # Unary if:
        # 1. First token
        # 2. Previous token is '('
        # 3. Previous token is an operator (except ')')
        if not prev_token:
            return True
        
        return prev_token in ('(', '**', '*', '/', '%', '+', '-')
    
    prev_token = None
    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        if token.replace('.', '', 1).isdigit():  # Number
            output.append(token)
            
        elif token == '(':
            stack.append(token)
            
        elif token == ')':
            # Pop until matching '('
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if not stack or stack[-1] != '(':
                raise ValueError("Unbalanced parentheses")
            stack.pop()  # Remove '('
            
        elif token in ('+', '-', '*', '/', '%', '**'):
            # Handle unary + and -
            if token in ('+', '-') and is_unary(token, prev_token):
                # Convert to unary operator
                unary_op = 'u+' if token == '+' else 'u-'
                stack.append(unary_op)
            else:
                # Binary operator
                while stack:
                    top = stack[-1]
                    if (is_operator(top) and 
                        (precedence(top) > precedence(token) or
                         (precedence(top) == precedence(token) and token != '**'))):
                        # For left-associative operators, pop when precedence is equal
                        # For right-associative '**', don't pop when precedence is equal
                        output.append(stack.pop())
                    else:
                        break
                stack.append(token)
        else:
            raise ValueError(f"Invalid token: {token}")
        
        prev_token = token
        i += 1
    
    # Pop remaining operators
    while stack:
        if stack[-1] == '(':
            raise ValueError("Unbalanced parentheses")
        output.append(stack.pop())
    
    return output


def evaluate_rpn(rpn: List[str]) -> float:
    """Evaluate RPN expression."""
    stack = []
    
    for token in rpn:
        if token.replace('.', '', 1).isdigit():  # Number
            stack.append(float(token))
        elif token == 'u+':  # Unary plus
            if not stack:
                raise ValueError("Invalid expression")
            # Unary plus doesn't change value
            val = stack.pop()
            stack.append(val)
        elif token == 'u-':  # Unary minus
            if not stack:
                raise ValueError("Invalid expression")
            val = stack.pop()
            stack.append(-val)
        else:  # Binary operator
            if len(stack) < 2:
                raise ValueError("Invalid expression")
            b = stack.pop()
            a = stack.pop()
            
            if token == '**':
                result = a ** b
            elif token == '*':
                result = a * b
            elif token == '/':
                if b == 0:
                    raise ValueError("Division by zero")
                result = a / b
            elif token == '%':
                if b == 0:
                    raise ValueError("Modulo by zero")
                result = a % b
            elif token == '+':
                result = a + b
            elif token == '-':
                result = a - b
            else:
                raise ValueError(f"Unknown operator: {token}")
            
            stack.append(result)
    
    if len(stack) != 1:
        raise ValueError("Invalid expression")
    
    return stack[0]