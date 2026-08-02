import re


def evaluate(expr: str) -> float:
    if expr is None:
        raise ValueError("Empty expression")
    s = expr
    i = 0
    n = len(s)
    tokens = []  # list of (type, value)

    while i < n:
        ch = s[i]
        if ch.isspace():
            i += 1
            continue
        if ch.isdigit():
            j = i
            while j < n and s[j].isdigit():
                j += 1
            if j < n and s[j] == '.':
                j2 = j + 1
                if j2 >= n or not s[j2].isdigit():
                    # decimal point must be followed by a digit
                    raise ValueError("Invalid number")
                j = j2
                while j < n and s[j].isdigit():
                    j += 1
            num_text = s[i:j]
            tokens.append(('NUM', float(num_text)))
            i = j
            continue
        # two-char operator **
        if ch == '*' and i + 1 < n and s[i + 1] == '*':
            tokens.append(('OP', '**'))
            i += 2
            continue
        if ch in '+-*/%()':
            if ch == '(':
                tokens.append(('LPAREN', ch))
            elif ch == ')':
                tokens.append(('RPAREN', ch))
            else:
                tokens.append(('OP', ch))
            i += 1
            continue
        # any other char is invalid
        raise ValueError(f"Invalid token: {ch}")

    if not tokens:
        raise ValueError("Empty expression")

    # Parser
    class Parser:
        def __init__(self, tokens):
            self.tokens = tokens
            self.pos = 0

        def peek(self):
            if self.pos < len(self.tokens):
                return self.tokens[self.pos]
            return ('EOF', None)

        def pop(self):
            tok = self.peek()
            self.pos += 1
            return tok

        def expect(self, kind, value=None):
            tok = self.peek()
            if tok[0] != kind or (value is not None and tok[1] != value):
                raise ValueError('Unexpected token')
            self.pop()

        def parse_expression(self):
            return self.parse_add_sub()

        def parse_add_sub(self):
            left = self.parse_mul_div()
            while True:
                tok = self.peek()
                if tok[0] == 'OP' and tok[1] in ('+', '-'):
                    op = tok[1]
                    self.pop()
                    right = self.parse_mul_div()
                    if op == '+':
                        left = left + right
                    else:
                        left = left - right
                else:
                    break
            return left

        def parse_mul_div(self):
            left = self.parse_unary()
            while True:
                tok = self.peek()
                if tok[0] == 'OP' and tok[1] in ('*', '/', '%'):
                    op = tok[1]
                    self.pop()
                    right = self.parse_unary()
                    if op == '*':
                        left = left * right
                    elif op == '/':
                        if right == 0:
                            raise ValueError('Division by zero')
                        left = left / right
                    elif op == '%':
                        if right == 0:
                            raise ValueError('Modulo by zero')
                        left = left % right
                else:
                    break
            return left

        def parse_unary(self):
            tok = self.peek()
            if tok[0] == 'OP' and tok[1] in ('+', '-'):
                op = tok[1]
                self.pop()
                val = self.parse_unary()
                return val if op == '+' else -val
            return self.parse_power()

        def parse_power(self):
            # base is primary
            left = self.parse_primary()
            tok = self.peek()
            if tok[0] == 'OP' and tok[1] == '**':
                self.pop()
                # right operand should be parsed as unary (so 2**-1 works)
                right = self.parse_unary()
                # right-associative: compute left ** right
                # However for chains like a**b**c, the recursion via parse_unary->parse_power handles it
                left = left ** right
            return left

        def parse_primary(self):
            tok = self.peek()
            if tok[0] == 'NUM':
                self.pop()
                return tok[1]
            if tok[0] == 'LPAREN':
                self.pop()
                val = self.parse_expression()
                if self.peek()[0] != 'RPAREN':
                    raise ValueError('Unbalanced parentheses')
                self.pop()
                return val
            raise ValueError('Unexpected token in primary')

    p = Parser(tokens)
    try:
        result = p.parse_expression()
    except IndexError:
        raise ValueError('Invalid expression')

    # after parsing ensure no leftover tokens
    if p.peek()[0] != 'EOF':
        # if only leftover is RPAREN or LPAREN or operator, it's an error
        raise ValueError('Invalid trailing tokens')

    try:
        return float(result)
    except Exception:
        raise ValueError('Could not compute result')
