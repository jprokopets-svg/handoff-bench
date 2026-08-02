def parse_json(text):
    """Parse a single strict JSON value from text and return the Python value.
    Raise ValueError on any invalid input.
    """
    if not isinstance(text, str):
        raise ValueError('input must be a string')

    s = text
    n = len(s)
    i = 0

    def err(msg='Invalid JSON'):
        raise ValueError(msg)

    def peek():
        return s[i] if i < n else None

    def advance():
        nonlocal i
        if i < n:
            ch = s[i]
            i += 1
            return ch
        return None

    def skip_ws():
        nonlocal i
        while i < n and s[i] in ' \t\n\r':
            i += 1

    def parse_value():
        nonlocal i
        skip_ws()
        if i >= n:
            err('Empty input')
        ch = s[i]
        if ch == '{':
            return parse_object()
        if ch == '[':
            return parse_array()
        if ch == '"':
            return parse_string()
        if ch == 't':
            return parse_literal('true', True)
        if ch == 'f':
            return parse_literal('false', False)
        if ch == 'n':
            return parse_literal('null', None)
        # number: must start with digit or -
        if ch == '-' or ('0' <= ch <= '9'):
            return parse_number()
        err('Unexpected character: {}'.format(ch))

    def parse_literal(lit, value):
        nonlocal i
        L = len(lit)
        if s[i:i+L] == lit:
            i_loc = i + L
            # ensure it's not part of identifier (though JSON only allows these literals)
            i_old = i
            i_new = i_loc
            i = i_loc
            return value
        err('Invalid literal')

    def parse_object():
        nonlocal i
        # assume current is '{'
        advance()  # consume '{'
        skip_ws()
        obj = {}
        if i < n and s[i] == '}':
            advance()
            return obj
        while True:
            skip_ws()
            if i >= n or s[i] != '"':
                err('Object keys must be strings')
            key = parse_string()
            skip_ws()
            if i >= n or s[i] != ':':
                err('Expected colon after key')
            advance()  # consume ':'
            val = parse_value()
            obj[key] = val
            skip_ws()
            if i >= n:
                err('Unclosed object')
            if s[i] == ',':
                advance()
                skip_ws()
                # trailing comma check: next must be a string key
                if i < n and s[i] == '}':
                    err('Trailing comma in object')
                continue
            elif s[i] == '}':
                advance()
                break
            else:
                err('Expected comma or } in object')
        return obj

    def parse_array():
        nonlocal i
        advance()  # consume '['
        skip_ws()
        arr = []
        if i < n and s[i] == ']':
            advance()
            return arr
        while True:
            val = parse_value()
            arr.append(val)
            skip_ws()
            if i >= n:
                err('Unclosed array')
            if s[i] == ',':
                advance()
                skip_ws()
                # trailing comma: next must not be ']'
                if i < n and s[i] == ']':
                    err('Trailing comma in array')
                continue
            elif s[i] == ']':
                advance()
                break
            else:
                err('Expected comma or ] in array')
        return arr

    def parse_string():
        nonlocal i
        # assume current is '"'
        if i >= n or s[i] != '"':
            err('Expected string')
        advance()  # consume opening quote
        chars = []
        while True:
            if i >= n:
                err('Unclosed string')
            ch = advance()
            if ch == '"':
                return ''.join(chars)
            if ch == '\\':
                if i >= n:
                    err('Unclosed string')
                esc = advance()
                if esc == '"':
                    chars.append('"')
                elif esc == '\\':
                    chars.append('\\')
                elif esc == '/':
                    chars.append('/')
                elif esc == 'b':
                    chars.append('\b')
                elif esc == 'f':
                    chars.append('\f')
                elif esc == 'n':
                    chars.append('\n')
                elif esc == 'r':
                    chars.append('\r')
                elif esc == 't':
                    chars.append('\t')
                elif esc == 'u':
                    # expect exactly 4 hex digits
                    if i+4-1 >= n:
                        err('Invalid unicode escape')
                    hex_digits = s[i:i+4]
                    for chh in hex_digits:
                        if not (chh.isdigit() or ('a' <= chh.lower() <= 'f')):
                            err('Invalid unicode escape')
                    # consume 4 digits
                    i_plus = i + 4
                    codepoint = int(hex_digits, 16)
                    chars.append(chr(codepoint))
                    # advance i by 4
                    nonlocal_i_set = None
                    # manually adjust i
                    # we can't rebind i via nonlocal in inner scope, so just set i
                    # but we are in same scope where i is nonlocal; modify directly
                    # (we are allowed to assign to i because declared nonlocal earlier)
                    i = i_plus
                else:
                    err('Invalid escape')
            else:
                # raw control characters not allowed
                if ord(ch) <= 0x1F:
                    err('Unescaped control character in string')
                chars.append(ch)

    def parse_number():
        nonlocal i
        start = i
        # optional minus
        if i < n and s[i] == '-':
            i += 1
            if i >= n:
                err('Invalid number')
        # integer part
        if i < n and s[i] == '0':
            i += 1
            int_leading_zero = True
        else:
            int_leading_zero = False
            if i < n and '1' <= s[i] <= '9':
                while i < n and s[i].isdigit():
                    i += 1
            else:
                err('Invalid number')
        # if leading zero followed by digit -> invalid
        if int_leading_zero:
            if i < n and s[i].isdigit():
                err('Leading zero in number')
        # fraction
        is_float = False
        if i < n and s[i] == '.':
            is_float = True
            i += 1
            if i >= n or not s[i].isdigit():
                err('Invalid fractional part')
            while i < n and s[i].isdigit():
                i += 1
        # exponent
        if i < n and (s[i] == 'e' or s[i] == 'E'):
            is_float = True
            i += 1
            if i < n and (s[i] == '+' or s[i] == '-'):
                i += 1
            if i >= n or not s[i].isdigit():
                err('Invalid exponent')
            while i < n and s[i].isdigit():
                i += 1
        num_str = s[start:i]
        try:
            if is_float:
                return float(num_str)
            else:
                return int(num_str)
        except Exception:
            err('Invalid number')

    # start parsing
    skip_ws()
    if i >= n:
        err('Empty input')
    value = parse_value()
    skip_ws()
    if i != n:
        err('Trailing data')
    return value
