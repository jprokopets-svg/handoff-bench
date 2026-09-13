import re

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
    def __repr__(self):
        return f"Token({self.type!r}, {self.value!r})"


def tokenize(s):
    tokens = []
    i = 0
    n = len(s)
    num_re = re.compile(r"\d+(?:\.\d+)?")
    while i < n:
        c = s[i]
        if c.isspace():
            i += 1
            continue
        if c.isdigit():
            m = num_re.match(s, i)
            if not m:
                raise ValueError("Invalid number")
            num = m.group(0)
            tokens.append(Token('NUMBER', float(num)))
            i = m.end()
            continue
        # two-char operator **
        if c == '*' and i+1 < n and s[i+1] == '*':
            tokens.append(Token('POW'))
            i += 2
            continue
        if c == '+':
            tokens.append(Token('PLUS'))
            i += 1
            continue
        if c == '-':
            tokens.append(Token('MINUS'))
            i += 1
            continue
        if c == '*':
            tokens.append(Token('MUL'))
            i += 1
            continue
        if c == '/':
            tokens.append(Token('DIV'))
            i += 1
            continue
        if c == '%':
            tokens.append(Token('MOD'))
            i += 1
            continue
        if c == '(':
            tokens.append(Token('LPAREN'))
            i += 1
            continue
        if c == ')':
            tokens.append(Token('RPAREN'))
            i += 1
            continue
        raise ValueError(f"Invalid token: {c}")
    tokens.append(Token('EOF'))
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos]

    def consume(self, type_=None):
        tok = self.current()
        if type_ and tok.type != type_:
            raise ValueError(f"Expected {type_}, got {tok.type}")
        self.pos += 1
        return tok

    def parse(self):
        if self.current().type == 'EOF':
            raise ValueError("Empty expression")
        val = self.parse_add_sub()
        if self.current().type != 'EOF':
            raise ValueError("Unexpected token")
        return val

    def parse_add_sub(self):
        val = self.parse_mul_div()
        while True:
            tok = self.current()
            if tok.type == 'PLUS':
                self.consume('PLUS')
                right = self.parse_mul_div()
                val = val + right
            elif tok.type == 'MINUS':
                self.consume('MINUS')
                right = self.parse_mul_div()
                val = val - right
            else:
                break
        return val

    def parse_mul_div(self):
        val = self.parse_unary()
        while True:
            tok = self.current()
            if tok.type == 'MUL':
                self.consume('MUL')
                right = self.parse_unary()
                val = val * right
            elif tok.type == 'DIV':
                self.consume('DIV')
                right = self.parse_unary()
                if right == 0:
                    raise ValueError('Division by zero')
                val = val / right
            elif tok.type == 'MOD':
                self.consume('MOD')
                right = self.parse_unary()
                if right == 0:
                    raise ValueError('Modulo by zero')
                val = val % right
            else:
                break
        return val

    def parse_unary(self):
        tok = self.current()
        if tok.type == 'PLUS':
            self.consume('PLUS')
            return +self.parse_unary()
        if tok.type == 'MINUS':
            self.consume('MINUS')
            return -self.parse_unary()
        return self.parse_power()

    def parse_power(self):
        # parse primary as base
        val = self.parse_primary()
        tok = self.current()
        if tok.type == 'POW':
            self.consume('POW')
            # right-associative: parse the right side allowing unary (which in turn will call parse_power),
            # so use parse_unary to allow constructs like 2**-1 and right-associativity via recursion
            right = self.parse_unary()
            val = val ** right
        return val

    def parse_primary(self):
        tok = self.current()
        if tok.type == 'NUMBER':
            self.consume('NUMBER')
            return tok.value
        if tok.type == 'LPAREN':
            self.consume('LPAREN')
            val = self.parse_add_sub()
            if self.current().type != 'RPAREN':
                raise ValueError('Unbalanced parentheses')
            self.consume('RPAREN')
            return val
        raise ValueError('Expected number or parenthesis')

def evaluate(s):
    tokens = tokenize(s)
    p = Parser(tokens)
    res = p.parse()
    return float(res)

# end of file
