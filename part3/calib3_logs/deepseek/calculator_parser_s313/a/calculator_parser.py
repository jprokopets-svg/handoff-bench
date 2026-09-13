import re
from typing import List, Union

def evaluate(expr: str) -> float:
    if not expr or expr.isspace():
        raise ValueError("Empty expression")
    
    # Tokenize the expression
    tokens = tokenize(expr)
    if not tokens:
        raise ValueError("Empty expression")
    
    # Check for basic syntax errors
    check_syntax(tokens)
    
    # Convert to RPN using shunting-yard algorithm
    rpn = shunting_yard(tokens)
    
    # Evaluate RPN
    return evaluate_rpn(rpn)


def tokenize(expr: str) -> List[Union[str, float]]:
    """Tokenize expression into numbers, operators, and parentheses."""
    # Regex to match numbers, operators, parentheses, and check for invalid characters
    token_pattern = re.compile(r"""
        \s*                         # Skip whitespace
        (                           # Capture groups:
          \d+(?:\.\d+)?             # Number (integer or decimal)
          | \*\*                    # Exponentiation operator
          | [+\-*/%()]              # Other operators and parentheses
          | [^\s\d+\-*/%()\.]       # Invalid character (will raise error)
        )
    """, re.VERBOSE)
    
    tokens = []
    pos = 0
    expr_len = len(expr)
    
    while pos < expr_len:
        # Skip whitespace
        if expr[pos].isspace():
            pos += 1
            continue
            
        # Try to match a token
        match = token_pattern.match(expr, pos)
        if not match:
            # Should not happen due to regex pattern
            raise ValueError(f"Invalid token at position {pos}")
        
        token = match.group(1)
        
        # Check for invalid character
        if re.match(r'[^\s\d+\-*/%()\.]', token) and token != '**':
            raise ValueError(f"Invalid token: {token}")
        
        # Convert number tokens to float
        if re.match(r'\d+(?:\.\d+)?$', token):
            tokens.append(float(token))
        else:
            tokens.append(token)
        
        pos = match.end()
    
    return tokens


def check_syntax(tokens: List[Union[str, float]]) -> None:
    """Check for syntax errors in tokens."""
    # Check for adjacent operands (two numbers in a row)
    for i in range(len(tokens) - 1):
        if isinstance(tokens[i], float) and isinstance(tokens[i + 1], float):
            raise ValueError("Adjacent operands without operator")
    
    # Check for trailing operator
    if tokens and isinstance(tokens[-1], str) and tokens[-1] not in ')':
        # Check if it's a binary operator (not unary)
        if tokens[-1] in '+-*/%**':
            # Check if it's actually a binary operator (not unary at end)
            # We need to determine if it's unary or binary
            # At the end of expression, any operator is invalid
            raise ValueError("Trailing operator")
    
    # Check for empty parentheses
    for i in range(len(tokens) - 1):
        if tokens[i] == '(' and tokens[i + 1] == ')':
            raise ValueError("Empty parentheses")
    
    # Check for invalid start
    if tokens and isinstance(tokens[0], str) and tokens[0] in '*/%**':
        raise ValueError("Expression starts with invalid operator")
    
    # Check parentheses balance
    balance = 0
    for token in tokens:
        if token == '(':
            balance += 1
        elif token == ')':
            balance -= 1
            if balance < 0:
                raise ValueError("Unbalanced parentheses")
    
    if balance != 0:
        raise ValueError("Unbalanced parentheses")


def precedence(op: str) -> int:
    """Return operator precedence."""
    if op == '**':
        return 4
    elif op in ('u+', 'u-'):  # Unary operators
        return 3
    elif op in ('*', '/', '%'):
        return 2
    elif op in ('+', '-'):
        return 1
    return 0


def is_unary_operator(tokens: List[Union[str, float]], index: int) -> bool:
    """Check if operator at given index is unary."""
    token = tokens[index]
    if token not in ('+', '-'):
        return False
    
    # Unary if:
    # 1. At start of expression
    if index == 0:
        return True
    
    # 2. After '('
    if tokens[index - 1] == '(':
        return True
    
    # 3. After another operator
    if isinstance(tokens[index - 1], str) and tokens[index - 1] not in ')':
        # Check if previous is an operator (not a number or closing paren)
        if tokens[index - 1] in '+-*/%**':
            return True
    
    return False


def shunting_yard(tokens: List[Union[str, float]]) -> List[Union[str, float]]:
    """Convert infix to RPN using shunting-yard algorithm."""
    output = []
    stack = []
    
    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        if isinstance(token, float):
            # Number
            output.append(token)
        
        elif token == '(':
            stack.append(token)
        
        elif token == ')':
            # Pop until '('
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if not stack:
                raise ValueError("Unbalanced parentheses")
            stack.pop()  # Remove '('
        
        else:  # Operator
            # Check if it's unary
            if token in ('+', '-') and is_unary_operator(tokens, i):
                # Replace with unary operator token
                op = 'u+' if token == '+' else 'u-'
            else:
                op = token
            
            # Handle right-associative **
            while stack and stack[-1] != '(':
                top = stack[-1]
                top_prec = precedence(top)
                op_prec = precedence(op)
                
                # For left-associative operators, pop if same or higher precedence
                # For right-associative **, only pop if higher precedence
                if (op != '**' and op_prec <= top_prec) or (op == '**' and op_prec < top_prec):
                    output.append(stack.pop())
                else:
                    break
            
            stack.append(op)
        
        i += 1
    
    # Pop remaining operators
    while stack:
        if stack[-1] == '(':
            raise ValueError("Unbalanced parentheses")
        output.append(stack.pop())
    
    return output


def evaluate_rpn(rpn: List[Union[str, float]]) -> float:
    """Evaluate RPN expression."""
    stack = []
    
    for token in rpn:
        if isinstance(token, float):
            stack.append(token)
        else:
            # Operator
            if token in ('u+', 'u-'):  # Unary operators
                if not stack:
                    raise ValueError("Invalid expression")
                a = stack.pop()
                if token == 'u+':
                    stack.append(a)
                else:  # 'u-'
                    stack.append(-a)
            else:  # Binary operators
                if len(stack) < 2:
                    raise ValueError("Invalid expression")
                b = stack.pop()
                a = stack.pop()
                
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    if b == 0:
                        raise ValueError("Division by zero")
                    stack.append(a / b)
                elif token == '%':
                    if b == 0:
                        raise ValueError("Modulo by zero")
                    stack.append(a % b)
                elif token == '**':
                    stack.append(a ** b)
    
    if len(stack) != 1:
        raise ValueError("Invalid expression")
    
    return stack[0]