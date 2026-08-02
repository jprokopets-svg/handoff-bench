import re

TOKEN_REGEX = re.compile(r"\s*(?:(\d+(?:\.\d+)?)|(\*\*)|([()+\-*/%])|(\S))")

class Parser:
    def __init__(self, text):
        self.text = text
        self.tokens = []
        self.pos = 0
        self._tokenize()

    def _tokenize(self):
        s = self.text
        i = 0
        while i < len(s):
            m = TOKEN_REGEX.match(s, i)
            if not m:
                # if only whitespace remains, break
                if s[i:].strip() == '':
                    break
                raise ValueError('Invalid token')
            num, powtok, single, bad = m.group(1,2,3,4)
            i = m.end()
            if num:
                self.tokens.append(('NUMBER', float(num)))
            elif powtok:
                # '**' matched in group 2
                self.tokens.append(('POW', '**'))
            elif single:
                ch = single
                if ch in '+-*/%()':
                    if ch == '+':
                        self.tokens.append(('PLUS','+'))
                    elif ch == '-':
                        self.tokens.append(('MINUS','-'))
                    elif ch == '*':
                        self.tokens.append(('MUL','*'))
                    elif ch == '/':
                        self.tokens.append(('DIV','/'))
                    elif ch == '%':
                        self.tokens.append(('MOD','%'))
                    elif ch == '(':
                        self.tokens.append(('LPAREN','('))
                    elif ch == ')':
                        self.tokens.append(('RPAREN',')'))
                else:
                    raise ValueError('Invalid token')
            elif bad:
                raise ValueError('Invalid token')
        # end while

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ('EOF', None)

    def next(self):
        tok = self.peek()
        self.pos += 1
        return tok

    def expect(self, kind):
        tok = self.peek()
        if tok[0] == kind:
            return self.next()
        raise ValueError('Expected %s' % kind)

    def parse(self):
        if not self.tokens:
            raise ValueError('Empty expression')
        val = self.parse_add()
        if self.pos != len(self.tokens):
            # leftover tokens -> error
            raise ValueError('Unexpected token')
        return val

    def parse_add(self):
        val = self.parse_mul()
        while True:
            tok = self.peek()
            if tok[0] == 'PLUS':
                self.next()
                rval = self.parse_mul()
                val = val + rval
            elif tok[0] == 'MINUS':
                self.next()
                rval = self.parse_mul()
                val = val - rval
            else:
                break
        return val

    def parse_mul(self):
        val = self.parse_unary()
        while True:
            tok = self.peek()
            if tok[0] == 'MUL':
                self.next()
                rval = self.parse_unary()
                val = val * rval
            elif tok[0] == 'DIV':
                self.next()
                rval = self.parse_unary()
                try:
                    if rval == 0:
                        raise ZeroDivisionError
                    val = val / rval
                except ZeroDivisionError:
                    raise ValueError('Division by zero')
            elif tok[0] == 'MOD':
                self.next()
                rval = self.parse_unary()
                try:
                    if rval == 0:
                        raise ZeroDivisionError
                    val = val % rval
                except ZeroDivisionError:
                    raise ValueError('Modulo by zero')
            else:
                break
        return val

    def parse_unary(self):
        tok = self.peek()
        if tok[0] == 'PLUS':
            self.next()
            return +self.parse_power()
        if tok[0] == 'MINUS':
            self.next()
            return -self.parse_power()
        return self.parse_power()

    def parse_power(self):
        # primary then optional '**' right-associative, with right operand parsed as unary
        left = self.parse_primary()
        tok = self.peek()
        if tok[0] == 'POW':
            self.next()
            right = self.parse_unary()
            try:
                left = left ** right
            except ZeroDivisionError:
                raise ValueError('Invalid power')
        return left

    def parse_primary(self):
        tok = self.peek()
        if tok[0] == 'NUMBER':
            self.next()
            return tok[1]
        if tok[0] == 'LPAREN':
            self.next()
            val = self.parse_add()
            if self.peek()[0] != 'RPAREN':
                raise ValueError('Mismatched parentheses')
            self.next()
            return val
        raise ValueError('Unexpected token')

def evaluate(expr):
    p = Parser(expr)
    try:
        return float(p.parse())
    except ValueError:
        raise
    except Exception:
        # any other exception treat as ValueError
        raise ValueError('Invalid expression')
