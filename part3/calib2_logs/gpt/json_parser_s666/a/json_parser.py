# Strict JSON parser
# Implements parse_json(text) -> Python object or raises ValueError on invalid input

def parse_json(text):
    if text is None:
        raise ValueError('Invalid input')
    s = text
    n = len(s)
    i = 0

    def skip_ws(idx):
        while idx < n and s[idx] in ' \t\n\r':
            idx += 1
        return idx

    def parse_value(idx):
        idx = skip_ws(idx)
        if idx >= n:
            raise ValueError('Unexpected end while parsing value')
        ch = s[idx]
        if ch == '{':
            return parse_object(idx)
        if ch == '[':
            return parse_array(idx)
        if ch == '"':
            return parse_string(idx)
        if ch == 'n' and s.startswith('null', idx):
            return (None, idx + 4)
        if ch == 't' and s.startswith('true', idx):
            return (True, idx + 4)
        if ch == 'f' and s.startswith('false', idx):
            return (False, idx + 5)
        if ch == '-' or ch.isdigit():
            return parse_number(idx)
        # Anything else is invalid
        raise ValueError(f'Invalid value at {idx}')

    def parse_object(idx):
        # s[idx] == '{'
        idx += 1
        idx = skip_ws(idx)
        obj = {}
        if idx < n and s[idx] == '}':
            return (obj, idx + 1)
        # else at least one pair
        while True:
            idx = skip_ws(idx)
            if idx >= n or s[idx] != '"':
                raise ValueError('Expected string key')
            key, idx = parse_string(idx)
            idx = skip_ws(idx)
            if idx >= n or s[idx] != ':':
                raise ValueError('Expected colon after key')
            idx += 1
            val, idx = parse_value(idx)
            obj[key] = val
            idx = skip_ws(idx)
            if idx >= n:
                raise ValueError('Unterminated object')
            if s[idx] == ',':
                # make sure not trailing comma before closing
                idx += 1
                idx = skip_ws(idx)
                if idx < n and s[idx] == '}':
                    raise ValueError('Trailing comma in object')
                continue
            elif s[idx] == '}':
                return (obj, idx + 1)
            else:
                raise ValueError('Expected comma or closing brace in object')

    def parse_array(idx):
        # s[idx] == '['
        idx += 1
        idx = skip_ws(idx)
        arr = []
        if idx < n and s[idx] == ']':
            return (arr, idx + 1)
        while True:
            val, idx = parse_value(idx)
            arr.append(val)
            idx = skip_ws(idx)
            if idx >= n:
                raise ValueError('Unterminated array')
            if s[idx] == ',':
                idx += 1
                idx = skip_ws(idx)
                if idx < n and s[idx] == ']':
                    raise ValueError('Trailing comma in array')
                continue
            elif s[idx] == ']':
                return (arr, idx + 1)
            else:
                raise ValueError('Expected comma or closing bracket in array')

    def parse_string(idx):
        # s[idx] == '"'
        idx += 1
        chars = []
        while True:
            if idx >= n:
                raise ValueError('Unterminated string')
            ch = s[idx]
            if ch == '"':
                return (''.join(chars), idx + 1)
            if ch == '\\':
                idx += 1
                if idx >= n:
                    raise ValueError('Unterminated escape')
                esc = s[idx]
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
                    # Expect exactly 4 hex digits
                    if idx + 4 >= n:
                        raise ValueError('Invalid unicode escape')
                    hexs = s[idx+1:idx+5]
                    if len(hexs) != 4 or any(c not in '0123456789abcdefABCDEF' for c in hexs):
                        raise ValueError('Invalid unicode escape')
                    codepoint = int(hexs, 16)
                    chars.append(chr(codepoint))
                    idx += 4
                else:
                    raise ValueError('Invalid escape')
                idx += 1
                continue
            # raw control chars are not allowed
            if ord(ch) <= 0x1F:
                raise ValueError('Unescaped control character in string')
            chars.append(ch)
            idx += 1

    def parse_number(idx):
        start = idx
        if s[idx] == '-':
            idx += 1
            if idx >= n:
                raise ValueError('Invalid number')
        # integer part
        if idx >= n:
            raise ValueError('Invalid number')
        if s[idx] == '0':
            int_start = idx
            idx += 1
            # if next is digit then leading zero
            if idx < n and s[idx].isdigit():
                raise ValueError('Leading zeros not allowed')
        else:
            if not s[idx].isdigit():
                raise ValueError('Invalid number')
            int_start = idx
            while idx < n and s[idx].isdigit():
                idx += 1
        has_frac = False
        has_exp = False
        # fraction
        if idx < n and s[idx] == '.':
            has_frac = True
            idx += 1
            if idx >= n or not s[idx].isdigit():
                raise ValueError('Invalid fraction')
            while idx < n and s[idx].isdigit():
                idx += 1
        # exponent
        if idx < n and (s[idx] == 'e' or s[idx] == 'E'):
            has_exp = True
            idx += 1
            if idx < n and (s[idx] == '+' or s[idx] == '-'):
                idx += 1
            if idx >= n or not s[idx].isdigit():
                raise ValueError('Invalid exponent')
            while idx < n and s[idx].isdigit():
                idx += 1
        num_str = s[start:idx]
        # Disallow forms like '1.' or '.5' are already handled: '.5' doesn't start number; '1.' would have '.' then no digits -> error
        try:
            if has_frac or has_exp:
                val = float(num_str)
            else:
                # integer
                val = int(num_str)
        except Exception:
            raise ValueError('Invalid number')
        return (val, idx)

    # parse top-level
    i = skip_ws(0)
    if i >= n:
        raise ValueError('Empty input')
    value, i = parse_value(i)
    i = skip_ws(i)
    if i != n:
        raise ValueError('Trailing content')
    return value
