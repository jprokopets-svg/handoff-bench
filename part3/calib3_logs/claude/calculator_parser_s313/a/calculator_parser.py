def evaluate(expr: str) -> float:
    """Evaluate an infix arithmetic expression and return the result as a float."""
    
    # Tokenize the expression
    tokens = tokenize(expr)
    
    if not tokens:
        raise ValueError("Empty expression")
    
    # Parse and evaluate using recursive descent parser
    parser = Parser(tokens)
    result = parser.parse_expression()
    
    # Ensure all tokens were consumed
    if parser.pos < len(parser.tokens):
        raise ValueError("Unexpected tokens after expression")
    
    return result


def tokenize(expr: str) -> list:
    """Tokenize the expression into a list of tokens."""
    tokens = []
    i = 0
    
    while i < len(expr):
        # Skip whitespace
        if expr[i].isspace():
            i += 1
            continue
        
        # Check for numbers (integers or decimals)
        if expr[i].isdigit():
            j = i
            while j < len(expr) and expr[j].isdigit():
                j += 1
            # Check for decimal point
            if j < len(expr) and expr[j] == '.':
                j += 1
                if j >= len(expr) or not expr[j].isdigit():
                    raise ValueError("Invalid number format")
                while j < len(expr) and expr[j].isdigit():
                    j += 1
            tokens.append(('NUMBER', float(expr[i:j])))
            i = j
            continue
        
        # Check for decimal starting with .
        if expr[i] == '.' and i + 1 < len(expr) and expr[i + 1].isdigit():
            raise ValueError("Decimal point must be preceded by a digit")
        
        # Check for operators and parentheses
        if expr[i] in '+-*/%()':
            tokens.append((expr[i], expr[i]))
            i += 1
            continue
        
        # Check for ** operator
        if expr[i] == '*' and i + 1 < len(expr) and expr[i + 1] == '*':
            tokens.append(('**', '**'))
            i += 2
            continue
        
        # Invalid character
        raise ValueError(f"Invalid token: {expr[i]}")
    
    return tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def current_token(self):
        """Get the current token without consuming it."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    
    def consume(self):
        """Consume and return the current token."""
        token = self.current_token()
        self.pos += 1
        return token
    
    def parse_expression(self):
        """Parse addition and subtraction (lowest precedence)."""
        left = self.parse_term()
        
        while self.current_token() and self.current_token()[0] in ['+', '-']:
            op = self.consume()[0]
            right = self.parse_term()
            if op == '+':
                left = left + right
            else:
                left = left - right
        
        return left
    
    def parse_term(self):
        """Parse multiplication, division, and modulo (middle precedence)."""
        left = self.parse_power()
        
        while self.current_token() and self.current_token()[0] in ['*', '/', '%']:
            op = self.consume()[0]
            right = self.parse_power()
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
    
    def parse_power(self):
        """Parse exponentiation (right-associative, higher precedence than unary)."""
        left = self.parse_unary()
        
        if self.current_token() and self.current_token()[0] == '**':
            self.consume()
            right = self.parse_power()  # Right-associative recursion
            left = left ** right
        
        return left
    
    def parse_unary(self):
        """Parse unary plus and minus (higher precedence than binary ops, lower than **)."""
        if self.current_token() and self.current_token()[0] in ['+', '-']:
            op = self.consume()[0]
            operand = self.parse_unary()  # Recursive for multiple unary operators
            if op == '-':
                return -operand
            else:
                return operand
        
        return self.parse_primary()
    
    def parse_primary(self):
        """Parse primary expressions: numbers and parenthesized expressions."""
        token = self.current_token()
        
        if not token:
            raise ValueError("Unexpected end of expression")
        
        # Number
        if token[0] == 'NUMBER':
            self.consume()
            return token[1]
        
        # Parenthesized expression
        if token[0] == '(':
            self.consume()
            result = self.parse_expression()
            if not self.current_token() or self.current_token()[0] != ')':
                raise ValueError("Unbalanced parentheses")
            self.consume()
            return result
        
        # Invalid token
        raise ValueError(f"Unexpected token: {token[0]}")
