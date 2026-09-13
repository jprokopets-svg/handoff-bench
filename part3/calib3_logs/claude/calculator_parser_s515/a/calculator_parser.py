def evaluate(expr: str) -> float:
    """
    Evaluate an infix arithmetic expression and return the numeric result as a float.
    
    Operators (highest to lowest precedence):
    - ** (right-associative, highest)
    - unary minus and unary plus
    - * / % (left-associative)
    - + - (left-associative, lowest)
    
    Parentheses group. Numbers may be integers or decimals.
    Whitespace is allowed anywhere.
    """
    
    # Tokenize the expression
    tokens = tokenize(expr)
    
    # Parse and evaluate using recursive descent parser
    parser = Parser(tokens)
    result = parser.parse_expression()
    
    # Ensure all tokens were consumed
    if parser.pos < len(parser.tokens):
        raise ValueError("Unexpected tokens after expression")
    
    return result


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    
    def consume(self, expected=None):
        token = self.current_token()
        if expected is not None and token != expected:
            raise ValueError(f"Expected {expected}, got {token}")
        self.pos += 1
        return token
    
    def parse_expression(self):
        """Parse addition and subtraction (lowest precedence)"""
        left = self.parse_term()
        
        while self.current_token() in ('+', '-'):
            op = self.consume()
            right = self.parse_term()
            if op == '+':
                left = left + right
            else:
                left = left - right
        
        return left
    
    def parse_term(self):
        """Parse multiplication, division, modulo (middle precedence)"""
        left = self.parse_unary()
        
        while self.current_token() in ('*', '/', '%'):
            op = self.consume()
            right = self.parse_unary()
            if op == '*':
                left = left * right
            elif op == '/':
                if right == 0:
                    raise ValueError("Division by zero")
                left = left / right
            else:  # op == '%'
                if right == 0:
                    raise ValueError("Modulo by zero")
                left = left % right
        
        return left
    
    def parse_unary(self):
        """Parse unary operators (minus and plus)"""
        if self.current_token() in ('+', '-'):
            op = self.consume()
            operand = self.parse_unary()
            if op == '-':
                return -operand
            else:
                return operand
        
        return self.parse_power()
    
    def parse_power(self):
        """Parse exponentiation (right-associative, highest precedence)"""
        left = self.parse_primary()
        
        if self.current_token() == '**':
            self.consume()
            # Right-associative: parse the right side recursively
            right = self.parse_power()
            return left ** right
        
        return left
    
    def parse_primary(self):
        """Parse primary expressions: numbers and parenthesized expressions"""
        token = self.current_token()
        
        if token is None:
            raise ValueError("Unexpected end of expression")
        
        # Handle parenthesized expressions
        if token == '(':
            self.consume()
            result = self.parse_expression()
            if self.current_token() != ')':
                raise ValueError("Unbalanced parentheses: missing ')'")
            self.consume()
            return result
        
        # Handle numbers
        if isinstance(token, (int, float)):
            self.consume()
            return float(token)
        
        raise ValueError(f"Invalid token: {token}")


def tokenize(expr: str):
    """Tokenize the expression into a list of tokens"""
    if not expr or expr.isspace():
        raise ValueError("Empty expression")
    
    tokens = []
    i = 0
    
    while i < len(expr):
        # Skip whitespace
        if expr[i].isspace():
            i += 1
            continue
        
        # Handle operators and parentheses
        if expr[i] in '()':
            tokens.append(expr[i])
            i += 1
        elif expr[i] in '+-*/%':
            # Check for ** operator
            if expr[i] == '*' and i + 1 < len(expr) and expr[i + 1] == '*':
                tokens.append('**')
                i += 2
            else:
                tokens.append(expr[i])
                i += 1
        elif expr[i].isdigit():
            # Parse number (integer or decimal)
            j = i
            while j < len(expr) and (expr[j].isdigit() or expr[j] == '.'):
                j += 1
            num_str = expr[i:j]
            
            # Validate the number format
            if num_str.count('.') > 1:
                raise ValueError(f"Invalid number: {num_str}")
            if num_str.startswith('.') or num_str.endswith('.'):
                raise ValueError(f"Invalid number: {num_str}")
            
            if '.' in num_str:
                tokens.append(float(num_str))
            else:
                tokens.append(int(num_str))
            i = j
        else:
            raise ValueError(f"Invalid character: {expr[i]}")
    
    if not tokens:
        raise ValueError("Empty expression")
    
    # Validate token sequence
    validate_tokens(tokens)
    
    return tokens


def validate_tokens(tokens):
    """Validate that the token sequence is valid"""
    if not tokens:
        raise ValueError("Empty expression")
    
    # Check for trailing operators
    last_token = tokens[-1]
    if last_token in ('+', '-', '*', '/', '%', '**', '('):
        raise ValueError("Trailing or incomplete operator")
    
    # Check for unbalanced parentheses and invalid sequences
    paren_depth = 0
    for i, token in enumerate(tokens):
        if token == '(':
            paren_depth += 1
        elif token == ')':
            paren_depth -= 1
            if paren_depth < 0:
                raise ValueError("Unbalanced parentheses: extra ')'")
        
        # Check for two adjacent operands (numbers without operator between them)
        if i > 0:
            prev_token = tokens[i - 1]
            curr_token = token
            
            # Both are numbers
            if isinstance(prev_token, (int, float)) and isinstance(curr_token, (int, float)):
                raise ValueError("Two adjacent operands without operator")
            
            # Number after closing paren, or opening paren after number
            if isinstance(prev_token, (int, float)) and curr_token == '(':
                raise ValueError("Two adjacent operands without operator")
            if prev_token == ')' and isinstance(curr_token, (int, float)):
                raise ValueError("Two adjacent operands without operator")
            if prev_token == ')' and curr_token == '(':
                raise ValueError("Two adjacent operands without operator")
    
    if paren_depth != 0:
        raise ValueError("Unbalanced parentheses: missing ')'")
