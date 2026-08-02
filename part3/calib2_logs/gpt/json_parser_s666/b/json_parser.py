def parse_json(text: str) -> object:
    if not isinstance(text, str):
        raise ValueError('input must be a string')
    n = len(text)
    pos = 0

    def skip_ws(i):
        while i < n and text[i] in ' \t\n\r':
            i += 1
        return i

    def parse_value(i):
        i = skip_ws(i)
        if i >= n:
            raise ValueError('Unexpected end of input while expecting a value')
        ch = text[i]
        if ch == '{':
            return parse_object(i)
        if ch == '[':
            return parse_array(i)
        if ch == '"':
            return parse_string(i)
        if ch == 't' and text.startswith('true', i):
            return True, i + 4
        if ch == 'f' and text.startswith('false', i):
            return False, i + 5
        if ch == 'n' and text.startswith('null', i):
            return None, i + 4
        # number
        if ch == '-' or ch.isdigit():
            return parse_number(i)
        raise ValueError(f'Invalid value starting at position {i}')

    def parse_object(i):
        # assumes text[i] == '{'
        i += 1
        i = skip_ws(i)
        obj = {}
        if i < n and text[i] == '}':
            return obj, i + 1
        while True:
            i = skip_ws(i)
            if i >= n or text[i] != '"':
                raise ValueError('Expected string for object key')
            key, i = parse_string(i)
            i = skip_ws(i)
            if i >= n or text[i] != ':':
                raise ValueError('Expected colon after object key')
            i += 1
            val, i = parse_value(i)
            obj[key] = val
            i = skip_ws(i)
            if i >= n:
                raise ValueError('Unterminated object')
            if text[i] == ',':
                # lookahead to forbid trailing comma before closing brace
                i += 1
                i = skip_ws(i)
                if i < n and text[i] == '}':
                    raise ValueError('Trailing comma in object')
                continue
            if text[i] == '}':
                return obj, i + 1
            raise ValueError('Expected comma or closing brace in object')

    def parse_array(i):
        # assumes text[i] == '['
        i += 1
        i = skip_ws(i)
        arr = []
        if i < n and text[i] == ']':
            return arr, i + 1
        while True:
            val, i = parse_value(i)
            arr.append(val)
            i = skip_ws(i)
            if i >= n:
                raise ValueError('Unterminated array')
            if text[i] == ',':
                i += 1
                i = skip_ws(i)
                if i < n and text[i] == ']':
                    raise ValueError('Trailing comma in array')
                continue
            if text[i] == ']':
                return arr, i + 1
            raise ValueError('Expected comma or closing bracket in array')

    def parse_string(i):
        # assumes text[i] == '"'
        i += 1
        chars = []
        while True:
            if i >= n:
                raise ValueError('Unterminated string')
            ch = text[i]
            if ch == '"':
                i += 1
                return ''.join(chars), i
            if ch == '\\':
                i += 1
                if i >= n:
                    raise ValueError('Unterminated escape')
                esc = text[i]
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
                    if i + 4 >= n:
                        raise ValueError('Invalid unicode escape')
                    hex_digits = text[i+1:i+5]
                    if len(hex_digits) != 4 or any(c not in '0123456789abcdefABCDEF' for c in hex_digits):
                        raise ValueError('Invalid unicode escape')
                    codepoint = int(hex_digits, 16)
                    chars.append(chr(codepoint))
                    i += 4
                else:
                    raise ValueError('Invalid escape character')
                i += 1
                continue
            # disallow raw control characters
            if ord(ch) <= 0x1F:
                raise ValueError('Unescaped control character in string')
            chars.append(ch)
            i += 1

    def parse_number(i):
        start = i
        if text[i] == '-':
            i += 1
            if i >= n:
                raise ValueError('Invalid number')
        # integer part
        if i < n and text[i] == '0':
            i += 1
            # leading zero must not be followed by digit
            if i < n and text[i].isdigit():
                raise ValueError('Leading zeros are not allowed')
        else:
            if i >= n or not text[i].isdigit():
                raise ValueError('Invalid number')
            while i < n and text[i].isdigit():
                i += 1
        is_float = False
        # fraction
        if i < n and text[i] == '.':
            is_float = True
            i += 1
            if i >= n or not text[i].isdigit():
                raise ValueError('Invalid number: digits required after decimal point')
            while i < n and text[i].isdigit():
                i += 1
        # exponent
        if i < n and (text[i] == 'e' or text[i] == 'E'):
            is_float = True
            i += 1
            if i < n and (text[i] == '+' or text[i] == '-'):
                i += 1
            if i >= n or not text[i].isdigit():
                raise ValueError('Invalid number: bad exponent')
            while i < n and text[i].isdigit():
                i += 1
        num_text = text[start:i]
        try:
            if is_float:
                val = float(num_text)
            else:
                val = int(num_text)
        except Exception:
            raise ValueError('Invalid number')
        return val, i

    pos = skip_ws(0)
    if pos >= n:
        raise ValueError('Empty input')
    value, pos = parse_value(pos)
    pos = skip_ws(pos)
    if pos != n:
        raise ValueError('Trailing data')
    return value
