import re

def parse_json(text):
    text = text.strip()
    if not text:
        raise ValueError("Empty input")

    def parse_value(s, i):
        i = skip_whitespace(s, i)
        res, new_i = parse_literal(s, i)
        if res is not None:
            return res, new_i
        res, new_i = parse_string(s, i)
        if res is not None:
            return res, new_i
        res, new_i = parse_number(s, i)
        if res is not None:
            return res, new_i
        res, new_i = parse_object(s, i)
        if res is not None:
            return res, new_i
        res, new_i = parse_array(s, i)
        if res is not None:
            return res, new_i
        return None, i

    def parse_string(s, i):
        if i >= len(s) or s[i] != '"':
            return None, i
        i += 1
        result = []
        while i < len(s):
            if s[i] == '"':
                return "".join(result), i + 1
            elif s[i] == '\\':
                i += 1
                if i >= len(s):
                    raise ValueError("Unterminated string")
                if s[i] == '"':
                    result.append('"')
                elif s[i] == '\\':
                    result.append('\\')
                elif s[i] == '/':
                    result.append('/')
                elif s[i] == 'b':
                    result.append('\b')
                elif s[i] == 'f':
                    result.append('\f')
                elif s[i] == 'n':
                    result.append('\n')
                elif s[i] == 'r':
                    result.append('\r')
                elif s[i] == 't':
                    result.append('\t')
                elif s[i] == 'u':
                    if i + 4 >= len(s):
                        raise ValueError("Invalid unicode escape")
                    hex_code = s[i+1:i+5]
                    if not re.fullmatch(r"[0-9a-fA-F]{4}", hex_code):
                        raise ValueError("Invalid unicode escape")
                    result.append(chr(int(hex_code, 16)))
                    i += 4
                else:
                    raise ValueError("Invalid escape sequence")
            elif ord(s[i]) < 32:
                raise ValueError("Unescaped control character")
            else:
                result.append(s[i])
            i += 1
        raise ValueError("Unterminated string")

    def parse_number(s, i):
        match = re.match(r"^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?", s[i:])
        if match:
            num_str = match.group(0)
            # No need for these checks, regex handles them
            # if num_str == '-' or num_str == '+' or num_str.endswith('.') or num_str.endswith('e') or num_str.endswith('E') or num_str.endswith('e-') or num_str.endswith('e+') or num_str.endswith('E-') or num_str.endswith('E+'):
            #     raise ValueError("Invalid number format")
            
            i += len(num_str)
            if '.' in num_str or 'e' in num_str or 'E' in num_str:
                return float(num_str), i
            return int(num_str), i
        return None, i

    def parse_object(s, i):
        if i >= len(s) or s[i] != '{':
            return None, i
        i += 1
        obj = {}
        i = skip_whitespace(s, i)
        if i >= len(s):
            raise ValueError("Unterminated object")
        if s[i] == '}':
            return obj, i + 1
        while True:
            key, i = parse_string(s, i)
            if key is None:
                raise ValueError("Expected string key")
            i = skip_whitespace(s, i)
            if i >= len(s) or s[i] != ':':
                raise ValueError("Expected ':'")
            i += 1
            i = skip_whitespace(s, i)
            value, i = parse_value(s, i)
            if value is None:
                raise ValueError("Expected value")
            obj[key] = value
            i = skip_whitespace(s, i)
            if i >= len(s):
                raise ValueError("Unterminated object")
            if s[i] == '}':
                return obj, i + 1
            if s[i] != ',':
                raise ValueError("Expected ',' or '}'")
            i += 1
            i = skip_whitespace(s, i)

    def parse_array(s, i):
        if i >= len(s) or s[i] != '[':
            return None, i
        i += 1
        arr = []
        i = skip_whitespace(s, i)
        if i >= len(s):
            raise ValueError("Unterminated array")
        if s[i] == ']':
            return arr, i + 1
        while True:
            value, i = parse_value(s, i)
            if value is None:
                raise ValueError("Expected value")
            arr.append(value)
            i = skip_whitespace(s, i)
            if i >= len(s):
                raise ValueError("Unterminated array")
            if s[i] == ']':
                return arr, i + 1
            if s[i] != ',':
                raise ValueError("Expected ',' or ']'")
            i += 1
            i = skip_whitespace(s, i)

    def parse_literal(s, i):
        if s[i:].startswith('true'):
            return True, i + 4
        if s[i:].startswith('false'):
            return False, i + 5
        if s[i:].startswith('null'):
            return None, i + 4
        return None, i

    def skip_whitespace(s, i):
        while i < len(s) and s[i].isspace():
            i += 1
        return i

    value, end_index = parse_value(text, 0)
    if value is None and text.strip() not in ["null", "true", "false", "[]", "{}"]:
        raise ValueError("Invalid JSON input")
    end_index = skip_whitespace(text, end_index)
    if end_index != len(text):
        raise ValueError("Trailing content after JSON value")
    return value
