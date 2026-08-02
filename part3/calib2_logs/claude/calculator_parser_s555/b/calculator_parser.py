import re
from typing import List, Tuple, Optional

def evaluate(expr: str) -> float:
    """Evaluate an infix arithmetic expression and return the result as a float."""
    tokens = tokenize(expr)
    if not tokens:
        raise ValueError("Empty expression")
    parser = Parser(tokens)
    result = parser.parse()
    if parser.pos < len(parser.tokens):
        raise ValueError("Unexpected token after expression")
    return result


def tokenize(expr: str) -> List[str]:
    """Tokenize the expression into operators, numbers, and parentheses."""
    # Pattern: numbers (int or decimal), operators, parentheses, or whitespace
    pattern = r'(\d+\.?\d*|\.\d+|[+\-*/%()]|[*]{2})'
    tokens = re.findall(pattern, expr)
    
    # Validate that the expression only contains valid tokens and whitespace
    remaining = re.sub(r'\s', '', expr)
    reconstructed = ''.join(tokens)
    if remaining != reconstructed:
        raise ValueError("Invalid token in expression")
    
    return tokens


class Parser:
    def __init__(self, tokens: List[str]):
        self.tokens = tokens
        self.pos = 0
    
    def parse(self) -> float:
        """Parse and evaluate the expression."""
        return self.expression()
    
    def current_token(self) -> Optional[str]:
        """Get the current token without consuming it."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    
    def consume(self, expected: Optional[str] = None) -> str:
        """Consume and return the current token."""
        token = self.current_token()
        if token is None:
            raise ValueError("Unexpected end of expression")
        if expected is not None and token != expected:
            raise ValueError(f"Expected {expected}, got {token}")
        self.pos += 1
        return token
    
    def expression(self) -> float:
        """Parse addition and subtraction (lowest precedence)."""
        left = self.term()
        
        while self.current_token() in ('+', '-'):
            op = self.consume()
            right = self.term()
            if op == '+':
                left = left + right
            else:
                left = left - right
        
        return left
    
    def term(self) -> float:
        """Parse multiplication, division, and modulo."""
        left = self.unary()
        
        while self.current_token() in ('*', '/', '%'):
            op = self.consume()
            right = self.unary()
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
    
    def unary(self) -> float:
        """Parse unary plus and minus."""
        if self.current_token() in ('+', '-'):
            op = self.consume()
            value = self.unary()  # Right-associative for unary operators
            if op == '-':
                return -value
            else:
                return value
        
        return self.power()
    
    def power(self) -> float:
        """Parse exponentiation (right-associative)."""
        left = self.primary()
        
        if self.current_token() == '**':
            self.consume('**')
            right = self.unary()  # Right-associative: parse unary to allow 2**-1
            return left ** right
        
        return left
    
    def primary(self) -> float:
        """Parse primary expressions: numbers and parenthesized expressions."""
        token = self.current_token()
        
        if token is None:
            raise ValueError("Unexpected end of expression")
        
        # Number
        if re.match(r'^\d+\.?\d*$', token) or re.match(r'^\.\d+$', token):
            self.consume()
            return float(token)
        
        # Parenthesized expression
        if token == '(':
            self.consume('(')
            result = self.expression()
            if self.current_token() != ')':
                raise ValueError("Unbalanced parentheses")
            self.consume(')')
            return result
        
        # Invalid token
        raise ValueError(f"Invalid token: {token}")
