from typing import List, Tuple, Union


class Token:
    def __init__(self, type_: str, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type!r}, {self.value!r})"


def tokenize(s: str) -> List[Token]:
    i = 0
    n = len(s)
    tokens: List[Token] = []
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
                j += 1
                # must have digits after the decimal
                if j >= n or not s[j].isdigit():
                    raise ValueError('Invalid number')
                while j < n and s[j].isdigit():
                    j += 1
            num_str = s[i:j]
            try:
                val = float(num_str)
            except Exception:
                raise ValueError('Invalid number')
            tokens.append(Token('NUMBER', val))
            i = j
            continue
        # operators and parentheses
        if ch in '+-*/%()':
            # handle '**'
            if ch == '*':
                if i + 1 < n and s[i + 1] == '*':
                    tokens.append(Token('OP', '**'))
                    i += 2
                    continue
                else:
                    tokens.append(Token('OP', '*'))
                    i += 1
                    continue
            elif ch in '+-/%':
                tokens.append(Token('OP', ch))
                i += 1
                continue
            elif ch == '/':
                tokens.append(Token('OP', '/'))
                i += 1
                continue
            elif ch == '(' or ch == ')':
                tokens.append(Token(ch))
                i += 1
                continue
        # any other char invalid
        raise ValueError('Invalid token')
    return tokens

def evaluate(expr: str) -> float:
    # tokenize
    tokens = tokenize(expr)
    if not tokens:
        raise ValueError('Empty expression')
    pos = 0

    def peek() -> Union[Token, None]:
        return tokens[pos] if pos < len(tokens) else None

    def consume(expected_type=None, expected_value=None) -> Token:
        nonlocal pos
        if pos >= len(tokens):
            raise ValueError('Unexpected end of expression')
        tok = tokens[pos]
        if expected_type is not None and tok.type != expected_type:
            raise ValueError('Unexpected token')
        if expected_value is not None and tok.value != expected_value:
            raise ValueError('Unexpected token')
        pos += 1
        return tok

    def parse_primary() -> float:
        tok = peek()
        if tok is None:
            raise ValueError('Unexpected end of expression')
        if tok.type == 'NUMBER':
            consume('NUMBER')
            return float(tok.value)
        if tok.type == '(':
            consume('(')
            val = parse_add()
            if peek() is None or peek().type != ')':
                raise ValueError('Unbalanced parentheses')
            consume(')')
            return val
        raise ValueError('Unexpected token')

    def parse_power() -> float:
        # primary ('**' parse_unary)? with right-assoc
        left = parse_primary()
        if peek() is not None and peek().type == 'OP' and peek().value == '**':
            consume('OP', '**')
            right = parse_unary()
            try:
                return left ** right
            except ZeroDivisionError:
                # propagate as ValueError
                raise ValueError('Math error')
        return left

    def parse_unary() -> float:
        tok = peek()
        if tok is not None and tok.type == 'OP' and tok.value in ('+', '-'):
            op = tok.value
            consume('OP', op)
            val = parse_unary()
            return val if op == '+' else -val
        return parse_power()

    def parse_mul() -> float:
        val = parse_unary()
        while True:
            tok = peek()
            if tok is not None and tok.type == 'OP' and tok.value in ('*', '/', '%'):
                op = tok.value
                consume('OP', op)
                rhs = parse_unary()
                if op == '*':
                    val
