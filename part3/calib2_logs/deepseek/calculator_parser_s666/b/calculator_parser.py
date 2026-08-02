import operator
import math

def evaluate(expr: str) -> float:
    """Evaluate an infix arithmetic expression and return the numeric result as a float."""
    
    # Remove whitespace
    expr = expr.strip()
    if not expr:
        raise ValueError("Empty expression")
    
    # Operator precedence and associativity
    # Higher number = higher precedence
    PRECEDENCE = {
        '**': 4,
        'u+': 3,  # unary plus
        'u-': 3,  # unary minus
        '*': 2,
        '/': 2,
        '%': 2,
        '+': 1,
        '-': 1,
    }
    
    # Right-associative operators
    RIGHT_ASSOC = {'**', 'u+', 'u-'}
    
    # Operator functions
    OPERATORS = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        '%': operator.mod,
        '**': operator.pow,
        'u+': lambda x: x,
        'u-': lambda x: -x,
    }
    
    def is_digit(ch: str) -> bool:
        return ch.isdigit()
    
    def is_number_start(ch: str) -> bool:
        return ch.isdigit() or ch == '.'
    
    def tokenize(expression: str):
        """Tokenize the expression into numbers, operators, and parentheses."""
        i = 0
        n = len(expression)
        tokens = []
        
        while i < n:
            ch = expression[i]
            
            # Skip whitespace
            if ch.isspace():
                i += 1
                continue
            
            # Number (integer or decimal)
            if is_number_start(ch):
                start = i
                dot_seen = False
                while i < n and (is_digit(expression[i]) or expression[i] == '.'):
                    if expression[i] == '.':
                        if dot_seen:
                            raise ValueError("Invalid number with multiple decimal points")
                        dot_seen = True
                    i += 1
                
                # Check if number ends with decimal point
                if expression[i-1] == '.':
                    raise ValueError("Invalid number ending with decimal point")
                
                num_str = expression[start:i]
                # Must have at least one digit before decimal point
                if num_str.startswith('.'):
                    raise ValueError("Number must have digit before decimal point")
                
                try:
                    tokens.append(float(num_str))
                except ValueError:
                    raise ValueError(f"Invalid number: {num_str}")
                continue
            
            # Parentheses
            if ch in '()':
                tokens.append(ch)
                i += 1
                continue
            
            # Operators
            if ch in '+-*/%':
                # Check for exponentiation operator '**'
                if ch == '*' and i + 1 < n and expression[i+1] == '*':
                    tokens.append('**')
                    i += 2
                    continue
                else:
                    tokens.append(ch)
                    i += 1
                    continue
            
            # Invalid character
            raise ValueError(f"Invalid character: {ch}")
        
        return tokens
    
    # Tokenize the expression
    try:
        tokens = tokenize(expr)
    except ValueError as e:
        raise ValueError(f"Invalid expression: {e}")
    
    # Convert to RPN using shunting-yard algorithm
    output = []
    stack = []
    
    # Helper to determine if a token is a unary operator
    def is_unary_operator(pos, token):
        """Determine if + or - is unary at position pos."""
        if token not in ('+', '-'):
            return False
        
        # At start of expression
        if pos == 0:
            return True
        
        # After '('
        if tokens[pos-1] == '(':
            return True
        
        # After another operator (including '**')
        if pos > 0 and isinstance(tokens[pos-1], str) and tokens[pos-1] not in ')':
            # Check if previous token is an operator (not a number or ')')
            # This includes all operators: '+', '-', '*', '/', '%', '**'
            return True
        
        return False
    
    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        # Number
        if isinstance(token, (int, float)):
            output.append(token)
        
        # Function or operator
        elif isinstance(token, str):
            if token == '(':
                stack.append(token)
            
            elif token == ')':
                # Pop until '(' is found
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                
                if not stack:
                    raise ValueError("Mismatched parentheses")
                
                # Remove '('
                stack.pop()
            
            else:
                # Handle unary + and -
                if token in ('+', '-') and is_unary_operator(i, token):
                    # Convert to unary operator token
                    token = 'u+' if token == '+' else 'u-'
                
                # While there's an operator at the top of the stack with greater precedence
                # or equal precedence and left-associative
                while stack and stack[-1] != '(' and stack[-1] in PRECEDENCE:
                    top_op = stack[-1]
                    
                    # Compare precedence
                    if (PRECEDENCE[top_op] > PRECEDENCE[token] or
                        (PRECEDENCE[top_op] == PRECEDENCE[token] and 
                         token not in RIGHT_ASSOC)):
                        output.append(stack.pop())
                    else:
                        break
                
                stack.append(token)
        
        i += 1
    
    # Pop remaining operators from stack
    while stack:
        op = stack.pop()
        if op == '(':
            raise ValueError("Mismatched parentheses")
        output.append(op)
    
    # Evaluate RPN
    eval_stack = []
    
    for token in output:
        if isinstance(token, (int, float)):
            eval_stack.append(token)
        else:
            # Operator
            if token in ('u+', 'u-'):
                # Unary operator
                if not eval_stack:
                    raise ValueError("Invalid expression: missing operand")
                a = eval_stack.pop()
                result = OPERATORS[token](a)
                eval_stack.append(result)
            else:
                # Binary operator
                if len(eval_stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands")
                b = eval_stack.pop()
                a = eval_stack.pop()
                
                # Check for division by zero
                if token == '/' and b == 0:
                    raise ValueError("Division by zero")
                if token == '%' and b == 0:
                    raise ValueError("Modulo by zero")
                
                result = OPERATORS[token](a, b)
                eval_stack.append(result)
    
    if len(eval_stack) != 1:
        raise ValueError("Invalid expression")
    
    return float(eval_stack[0])