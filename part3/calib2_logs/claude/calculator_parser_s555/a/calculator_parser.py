def evaluate(expr: str) -> float:
    """
    Evaluate an infix arithmetic expression and return the result as a float.
    
    Operator precedence (highest to lowest):
    1. ** (right-associative)
    2. unary minus and unary plus
    3. * / % (left-associative)
    4. + - (left-associative)
    
    Parentheses group expressions.
    """
    tokens = tokenize(expr)
    if not tokens:
        raise ValueError("Empty expression")
    
    parser = Parser(tokens)
    result = parser.parse_expression()
    
    if parser.pos < len(parser.tokens):
        raise ValueError("Unexpected token after expression")
    
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
        
        # Numbers (integers or decimals)
        if expr[i].isdigit():
            j = i
            while j < len(expr) and expr[j].isdigit():
                j += 1
            if j < len(expr) and expr[j] == '.':
                j += 1
                while j < len(expr) and expr[j].isdigit():
                    j += 1
            tokens.append(('NUMBER', float(expr[i:j])))
            i = j
            continue
        
        # Power operator
        if i + 1 < len(expr) and expr[i:i+2] == '**':
            tokens.append(('**', '**'))
            i += 2
            continue
        
        # Operators and parentheses
        if expr[i] in '+-*/()%':
            tokens.append((expr[i], expr[i]))
            i += 1
            continue
        
        # Invalid character
        raise ValueError(f"Invalid token: {expr[i]}")
    
    return tokens


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
        if token is None:
            raise ValueError("Unexpected end of expression")
        if expected and token[0] != expected:
            raise ValueError(f"Expected {expected}, got {token[0]}")
        self.pos += 1
        return token
    
    def parse_expression(self):
        """Parse addition and subtraction (lowest precedence)."""
        left = self.parse_term()
        
        while self.current_token() and self.current_token()[0] in ('+', '-'):
            op = self.consume()[0]
            right = self.parse_term()
            if op == '+':
                left = left + right
            else:
                left = left - right
        
        return left
    
    def parse_term(self):
        """Parse multiplication, division, and modulo."""
        left = self.parse_unary()
        
        while self.current_token() and self.current_token()[0] in ('*', '/', '%'):
            op = self.consume()[0]
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
        """Parse unary plus and minus (higher precedence than * / %)."""
        if self.current_token() and self.current_token()[0] in ('+', '-'):
            op = self.consume()[0]
            operand = self.parse_unary()  # Recursive for chaining unary operators
            if op == '-':
                operand = -operand
            return operand
        
        return self.parse_power()
    
    def parse_power(self):
        """Parse exponentiation (right-associative, highest precedence)."""
        left = self.parse_primary()
        
        # Handle ** (right-associative)
        if self.current_token() and self.current_token()[0] == '**':
            self.consume('**')
            right = self.parse_unary()  # After **, unary operators bind
            left = left ** right
        
        return left
    
    def parse_primary(self):
        """Parse primary expressions: numbers and parenthesized expressions."""
        token = self.current_token()
        
        if token is None:
            raise ValueError("Unexpected end of expression")
        
        # Number
        if token[0] == 'NUMBER':
            self.consume()
            return token[1]
        
        # Parenthesized expression
        if token[0] == '(':
            self.consume('(')
            result = self.parse_expression()
            if self.current_token() is None or self.current_token()[0] != ')':
                raise ValueError("Unbalanced parentheses")
            self.consume(')')
            return result
        
        raise ValueError(f"Unexpected token: {token[0]}")
