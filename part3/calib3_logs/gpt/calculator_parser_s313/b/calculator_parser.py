import re
from typing import Optional

# Token types
NUMBER = 'NUMBER'
PLUS = 'PLUS'
MINUS = 'MINUS'
MUL = 'MUL'
DIV = 'DIV'
MOD = 'MOD'
POW = 'POW'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
EOF = 'EOF'

class Token:
    def __init__(self, type_, value: Optional[float] = None):
        self.type = type_
        self.value = value
    def __repr__(self):
        return f"Token({self.type}, {self.value})"

def tokenize(s: str):
    i = 0
    n = len(s)
    tokens = []
    number_re = re.compile(r"\d+(?:\.\d+)?")
    while i < n:
        ch = s[i]
        if ch.isspace():
            i += 1
            continue
        if ch.isdigit():
            m = number_re.match(s, i)
            if not m:
                raise ValueError('Invalid number')
            num = float(m.group(0))
            tokens.append(Token(NUMBER, num))
            i = m.end()
            continue
        # two-char operator **
        if ch == '*':
            if i + 1 < n and s[i+1] == '*':
                tokens.append(Token(POW))
                i += 2
            else:
                tokens.append(Token(MUL))
                i += 1
            continue
        if ch == '+':
            tokens.append(Token(PLUS))
            i += 1
            continue
        if ch == '-':
            tokens.append(Token(MINUS))
            i += 1
            continue
        if ch == '/':
            tokens.append(Token(DIV))
            i += 1
            continue
        if ch == '%':
            tokens.append(Token(MOD))
            i += 1
            continue
        if ch == '(':
            tokens.append(Token(LPAREN))
            i += 1
            continue
        if ch == ')':
            tokens.append(Token(RPAREN))
            i += 1
            continue
        # anything else invalid
        raise ValueError(f'Invalid token: {ch}')
    tokens.append(Token(EOF))
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current = tokens[0]

    def eat(self, type_):
        if self.current.type == type_:
            self.pos += 1
            self.current = self.tokens[self.pos]
        else:
            raise ValueError('Unexpected token')

    def parse(self):
        if self.current.type == EOF:
            raise ValueError('Empty expression')
        result = self.expr()
        if self.current.type != EOF:
            raise ValueError('Unexpected token')
        return result

    # expression -> add_sub
    def expr(self):
        return self.add_sub()

    # add_sub -> mul_div ( (PLUS|MINUS) mul_div )*
    def add_sub(self):
        result = self.mul_div()
        while self.current.type in (PLUS, MINUS):
            tok = self.current.type
            self.eat(tok)
            rhs = self.mul_div()
            if tok == PLUS:
                result = result + rhs
            else:
                result = result - rhs
        return result

    # mul_div -> unary ( (MUL|DIV|MOD) unary )*
    def mul_div(self):
        result = self.unary()
        while self.current.type in (MUL, DIV, MOD):
            tok = self.current.type
            self.eat(tok)
            rhs = self.unary()
            if tok == MUL:
                result = result * rhs
            elif tok == DIV:
                if rhs == 0:
                    raise ValueError('Division by zero')
                result = result / rhs
            else:  # MOD
                if rhs == 0:
                    raise ValueError('Modulo by zero')
                result = result % rhs
        return result

    # unary -> (PLUS|MINUS) unary | power
    def unary(self):
        if self.current.type == PLUS:
            self.eat(PLUS)
            return +self.unary()
        if self.current.type == MINUS:
            self.eat(MINUS)
            return -self.unary()
        return self.power()

    # power -> primary (POW power)?   right-associative
    def power(self):
        left = self.primary()
        if self.current.type == POW:
            self.eat(POW)
            right = self.power()
            # pow handles negative exponents and floats
            return left ** right
        return left

    # primary -> NUMBER | LPAREN expr RPAREN
    def primary(self):
        if self.current.type == NUMBER:
            val = self.current.value
            self.eat(NUMBER)
            return val
        if self.current.type == LPAREN:
            self.eat(LPAREN)
            val = self.expr()
            if self.current.type != RPAREN:
                raise ValueError('Unbalanced parentheses')
            self.eat(RPAREN)
            return val
        raise ValueError('Unexpected token in primary')


def evaluate(expr: str) -> float:
    tokens = tokenize(expr)
    p = Parser(tokens)
    result = p.parse()
    return float(result)
