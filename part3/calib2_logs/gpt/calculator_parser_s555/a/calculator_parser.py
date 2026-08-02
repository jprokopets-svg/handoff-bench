# calculator_parser.py

def evaluate(expr: str) -> float:
    """Evaluate arithmetic expression and return float result.
    Raises ValueError on invalid input or division/modulo by zero.
    """
    if expr is None:
        raise ValueError("Empty expression")
    s = expr
    # Tokenize
    tokens = []  # list of (type, value)
    i = 0
    n = len(s)
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
                k = j
                while k < n and s[k].isdigit():
                    k += 1
                if k == j:
                    raise ValueError('Invalid number')
                num_str = s[i:k]
                i = k
            else:
                num_str = s[i:j]
                i = j
            try:
                val = float(num_str)
            except Exception:
                raise ValueError('Invalid number')
            tokens.append(('NUM', val))
            continue
        if ch == '*' and i + 1 < n and s[i+1] == '*':
            tokens.append(('OP', '**'))
            i += 2
            continue
        if ch in '+-*/%()':
            if ch == '(':
                tokens.append(('LP', ch))
            elif ch == ')':
                tokens.append(('RP', ch))
            else:
                tokens.append(('OP', ch))
            i += 1
            continue
        # anything else is invalid
        raise ValueError(f'Invalid token: {ch}')

    # Parser
    idx = 0
    L = len(tokens)

    def peek():
        return tokens[idx] if idx < L else None

    def advance():
        nonlocal idx
        tok = tokens[idx] if idx < L else None
        idx += 1
        return tok

    def parse_expression():
        return parse_add_sub()

    def parse_add_sub():
        nonlocal idx
        left = parse_mul_div()
        while True:
            t = peek()
            if t and t[0] == 'OP' and t[1] in ('+', '-'):
                op = advance()[1]
                right = parse_mul_div()
                if op == '+':
                    left = left + right
                else:
                    left = left - right
            else:
                break
        return left

    def parse_mul_div():
        nonlocal idx
        left = parse_factor()
        while True:
            t = peek()
            if t and t[0] == 'OP' and t[1] in ('*', '/', '%'):
                op = advance()[1]
                right = parse_factor()
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

    def parse_factor():
        # handle unary + and -; unary binds looser than ** due to power parsing using factor as rhs
        t = peek()
        if t and t[0] == 'OP' and t[1] in ('+', '-'):
            op = advance()[1]
            val = parse_factor()
            return val if op == '+' else -val
        return parse_power()

    def parse_power():
        # primary ('**' factor)? right associative
        left = parse_primary()
        t = peek()
        if t and t[0] == 'OP' and t[1] == '**':
            advance()
            right = parse_factor()
            # python's pow with floats
            left = left ** right
        return left

    def parse_primary():
        t = peek()
        if t is None:
            raise ValueError('Unexpected end of expression')
        if t[0] == 'NUM':
            advance()
            return t[1]
        if t[0] == 'LP':
            advance()
            val = parse_expression()
            t2 = peek()
            if t2 and t2[0] == 'RP':
                advance()
                return val
            else:
                raise ValueError('Unbalanced parentheses')
        # anything else (like RP or OP where operand expected)
        raise ValueError('Unexpected token')

    # Start parse
    if L == 0:
        raise ValueError('Empty expression')
    val = parse_expression()
    if idx != L:
        # leftover tokens
        raise ValueError('Invalid syntax')
    # ensure float
    try:
        return float(val)
    except Exception:
        raise ValueError('Invalid result')
