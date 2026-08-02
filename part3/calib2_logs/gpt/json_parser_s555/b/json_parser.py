def parse_json(text: str) -> object:
    """
    Strict JSON parser for a single value. Raises ValueError on invalid input.
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    class Parser:
        def __init__(self, s: str):
            self.s = s
            self.i = 0
            self.n = len(s)

        def skip_ws(self):
            while self.i < self.n and self.s[self.i] in " \t\n\r":
                self.i += 1

        def peek(self):
            return self.s[self.i] if self.i < self.n else None

        def advance(self):
            ch = self.peek()
            if ch is None:
                raise ValueError("Unexpected end of input")
            self.i += 1
            return ch

        def expect_char(self, ch):
            if self.peek() != ch:
                raise ValueError(f"Expected '{ch}' at position {self.i}")
            self.i += 1

        def parse_value(self):
            self.skip_ws()
            ch = self.peek()
            if ch is None:
                raise ValueError("Empty input or unexpected end")
            if ch == '{':
                return self.parse_object()
            if ch == '[':
                return self.parse_array()
            if ch == '"':
                return self.parse_string()
            if ch == 'n' or ch == 't' or ch == 'f':
                return self.parse_literal()
            # number can start with '-' or digit
            if ch == '-' or ch.isdigit():
                return self.parse_number()
            raise ValueError(f"Invalid value at position {self.i}")

        def parse_object(self):
            # assumes current char is '{'
            self.expect_char('{')
            obj = {}
            self.skip_ws()
            if self.peek() == '}':
                self.i += 1
                return obj
            while True:
                self.skip_ws()
                if self.peek() != '"':
                    raise ValueError(f"Object keys must be strings at position {self.i}")
                key = self.parse_string()
                self.skip_ws()
                if self.peek() != ':':
                    raise ValueError(f"Expected ':' after key at position {self.i}")
                self.i += 1
                val = self.parse_value()
                obj[key] = val
                self.skip_ws()
                ch = self.peek()
                if ch == ',':
                    # detect trailing comma by ensuring next non-ws is not '}'
                    self.i += 1
                    self.skip_ws()
                    if self.peek() == '}' or self.peek() is None:
                        raise ValueError("Trailing comma in object")
                    continue
                if ch == '}':
                    self.i += 1
                    break
                raise ValueError(f"Expected ',' or '}}' in object at position {self.i}")
            return obj

        def parse_array(self):
            # assumes current char is '['
            self.expect_char('[')
            arr = []
            self.skip_ws()
            if self.peek() == ']':
                self.i += 1
                return arr
            while True:
                val = self.parse_value()
                arr.append(val)
                self.skip_ws()
                ch = self.peek()
                if ch == ',':
                    self.i += 1
                    self.skip_ws()
                    if self.peek() == ']' or self.peek() is None:
                        raise ValueError("Trailing comma in array")
                    continue
                if ch == ']':
                    self.i += 1
                    break
                raise ValueError(f"Expected ',' or ']' in array at position {self.i}")
            return arr

        def parse_string(self):
            # assumes current char is '"'
            self.expect_char('"')
            parts = []
            s = self.s
            while True:
                if self.i >= self.n:
                    raise ValueError("Unterminated string")
                ch = s[self.i]
                if ch == '"':
                    self.i += 1
                    return ''.join(parts)
                if ch == '\\':
                    # escape
                    self.i += 1
                    if self.i >= self.n:
                        raise ValueError("Unterminated escape")
                    esc = s[self.i]
                    self.i += 1
                    if esc == '"':
                        parts.append('"')
                    elif esc == '\\':
                        parts.append('\\')
                    elif esc == '/':
                        parts.append('/')
                    elif esc == 'b':
                        parts.append('\b')
                    elif esc == 'f':
                        parts.append('\f')
                    elif esc == 'n':
                        parts.append('\n')
                    elif esc == 'r':
                        parts.append('\r')
                    elif esc == 't':
                        parts.append('\t')
                    elif esc == 'u':
                        # expect 4 hex digits
                        if self.i + 4 > self.n:
                            raise ValueError("Invalid \\u escape (too short)")
                        hex4 = s[self.i:self.i+4]
                        for c in hex4:
                            if c not in '0123456789abcdefABCDEF':
                                raise ValueError("Invalid \\u escape (bad hex)")
                        code = int(hex4, 16)
                        self.i += 4
                        # handle surrogate pairs
                        if 0xD800 <= code <= 0xDBFF:
                            # must be followed by another \uXXXX low surrogate
                            if self.i + 6 <= self.n and s[self.i] == '\\' and s[self.i+1] == 'u':
                                low_hex = s[self.i+2:self.i+6]
                                valid_low = True
                                for c in low_hex:
                                    if c not in '0123456789abcdefABCDEF':
                                        valid_low = False
                                        break
                                if valid_low:
                                    low = int(low_hex, 16)
                                    if 0xDC00 <= low <= 0xDFFF:
                                        # consume low surrogate
                                        self.i += 6
                                        codepoint = 0x10000 + ((code - 0xD800) << 10) + (low - 0xDC00)
                                        parts.append(chr(codepoint))
                                        continue
                            # invalid surrogate pair
                            raise ValueError("Invalid \\u surrogate pair")
                        else:
                            parts.append(chr(code))
                    else:
                        raise ValueError(f"Invalid escape '\\{esc}'")
                else:
                    # raw character
                    # control characters not allowed
                    if ord(ch) < 0x20:
                        raise ValueError("Invalid control character in string")
                    parts.append(ch)
                    self.i += 1

        def parse_number(self):
            s = self.s
            start = self.i
            # optional minus
            if self.peek() == '-':
                self.i += 1
            # integer part
            if self.i >= self.n:
                raise ValueError("Invalid number")
            if s[self.i] == '0':
                self.i += 1
                # leading zero must not be followed by digit
                if self.i < self.n and s[self.i].isdigit():
                    raise ValueError("Leading zeros are not allowed")
            else:
                if not s[self.i].isdigit():
                    raise ValueError("Invalid number")
                while self.i < self.n and s[self.i].isdigit():
                    self.i += 1
            is_float = False
            # fraction
            if self.i < self.n and s[self.i] == '.':
                is_float = True
                self.i += 1
                if self.i >= self.n or not s[self.i].isdigit():
                    raise ValueError("Invalid fractional part")
                while self.i < self.n and s[self.i].isdigit():
                    self.i += 1
            # exponent
            if self.i < self.n and (s[self.i] == 'e' or s[self.i] == 'E'):
                is_float = True
                self.i += 1
                if self.i < self.n and (s[self.i] == '+' or s[self.i] == '-'):
                    # plus sign allowed in exponent
                    self.i += 1
                if self.i >= self.n or not s[self.i].isdigit():
                    raise ValueError("Invalid exponent")
                while self.i < self.n and s[self.i].isdigit():
                    self.i += 1
            num_text = s[start:self.i]
            try:
                if is_float:
                    return float(num_text)
                else:
                    return int(num_text)
            except Exception:
                raise ValueError("Invalid number conversion")

        def parse_literal(self):
            # null, true, false
            s = self.s
            if s.startswith('null', self.i):
                end = self.i + 4
                if end < self.n and (s[end].isalpha() or s[end].isdigit() or s[end] == '_'):
                    raise ValueError("Invalid token")
                self.i = end
                return None
            if s.startswith('true', self.i):
                end = self.i + 4
                if end < self.n and (s[end].isalpha() or s[end].isdigit() or s[end] == '_'):
                    raise ValueError("Invalid token")
                self.i = end
                return True
            if s.startswith('false', self.i):
                end = self.i + 5
                if end < self.n and (s[end].isalpha() or s[end].isdigit() or s[end] == '_'):
                    raise ValueError("Invalid token")
                self.i = end
                return False
            raise ValueError(f"Invalid literal at position {self.i}")

    p = Parser(text)
    p.skip_ws()
    if p.i >= p.n:
        raise ValueError("Empty input")
    val = p.parse_value()
    p.skip_ws()
    if p.i != p.n:
        raise ValueError("Trailing data")
    return val
