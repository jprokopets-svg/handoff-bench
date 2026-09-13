import re

number_re = re.compile(r"\d+(?:\.\d+)?")

class ParseError(ValueError):
    pass


def tokenize(expr: str):
    if expr is None:
        raise ParseError("Invalid expression")
    tokens = []
    i = 0
    n = len(expr)
    while i < n:
        ch = expr[i]
        if ch.isspace():
            i += 1
            continue
        if ch.isdigit():
            m = number_re.match(expr, i)
            if not m:
                raise ParseError("Invalid number")
            tok = m.group(0)
            tokens.append(('NUMBER', tok))
            i = m.end()
            continue
        if expr.startswith('**', i):
            tokens.append(('OP', '**'))
            i += 2
            continue
        if ch in '+-*/%()':
            tokens.append(('OP', ch))
            i += 1
            continue
        # any other character is invalid (including leading dot numbers or letters)
        raise ParseError(f"Invalid token: {ch}")
    return tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def next(self):
        t = self.peek()
        if t is None:
            return None
        self.pos += 1
        return t

    # expression -> add_sub
    def parse_expression(self):
        val = self.parse_add_sub()
        return val

    # add_sub -> mult_div (('+'|'-') mult_div)*
    def parse_add_sub(self):
        val = self.parse_mul_div()
        while True:
            t = self.peek()
            if t and t[0] == 'OP' and t[1] in ('+', '-'):
                op = t[1]
                self.next()
                rhs = self.parse_mul_div()
                if op == '+':
                    val = val + rhs
                else:
                    val = val - rhs
            else:
                break
        return val

    # mul_div -> factor (('*'|'/'|'%') factor)*
    def parse_mul_div(self):
        val = self.parse_factor()
        while True:
            t = self.peek()
            if t and t[0] == 'OP' and t[1] in ('*', '/', '%'):
                op = t[1]
                self.next()
                rhs = self.parse_factor()
                if op == '*':
                    val = val * rhs
                elif op == '/':
                    if rhs == 0:
                        raise ParseError('Division by zero')
                    val = val / rhs
                else:  # %
                    if rhs == 0:
                        raise ParseError('Modulo by zero')
                    # Python's modulo with floats behaves like desired
                    val = val % rhs
            else:
                break
        return val

    # factor -> ('+'|'-') factor | power
    def parse_factor(self):
        t = self.peek()
        if t and t[0] == 'OP' and t[1] in ('+', '-'):
            op = t[1]
            self.next()
            val = self.parse_factor()
            if op == '+':
                return +val
            else:
                return -val
        else:
            return self.parse_power()

    # power -> primary ('**' factor)?  (right-assoc, allows unary in exponent)
    def parse_power(self):
        val = self.parse_primary()
        t = self.peek()
        if t and t[0] == 'OP' and t[1] == '**':
            self.next()
            rhs = self.parse_factor()
            # right-associative: compute val ** rhs
            # ensure float conversion
            try:
                val = val ** rhs
            except ZeroDivisionError:
                # unlikely here
                raise
        return val

    # primary -> NUMBER | '(' expression ')'
    def parse_primary(self):
        t = self.peek()
        if t is None:
            raise ParseError('Unexpected end of expression')
        if t[0] == 'NUMBER':
            self.next()
            return float(t[1])
        if t[0] == 'OP' and t[1] == '(':
            self.next()
            val = self.parse_expression()
            t2 = self.peek()
            if t2 and t2[0] == 'OP' and t2[1] == ')':
                self.next()
                return val
            else:
                raise ParseError('Unbalanced parentheses')
        raise ParseError(f"Unexpected token: {t}")


def evaluate(expr: str) -> float:
    tokens = tokenize(expr)
    if not tokens:
        raise ValueError('Empty expression')
    p = Parser(tokens)
    try:
        val = p.parse_expression()
    except ParseError as e:
        raise ValueError(str(e))
    # if not all tokens consumed -> error (e.g., '1 2')
    if p.peek() is not None:
        raise ValueError('Invalid expression')
    # final result must be float
    return float(val)
