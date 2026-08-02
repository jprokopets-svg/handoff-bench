def parse_json(text: str) -> object:
    """Parse a JSON string and return the corresponding Python object.
    
    Raises ValueError if the input is not valid JSON.
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    
    # Create a parser state object to track position and handle errors
    class Parser:
        def __init__(self, text):
            self.text = text
            self.pos = 0
            self.length = len(text)
        
        def peek(self):
            """Return the current character without advancing."""
            if self.pos < self.length:
                return self.text[self.pos]
            return None
        
        def consume(self, expected=None):
            """Consume and return the current character.
            
            If expected is provided, raise ValueError if the character doesn't match.
            """
            if self.pos >= self.length:
                raise ValueError("Unexpected end of input")
            ch = self.text[self.pos]
            if expected is not None and ch != expected:
                raise ValueError(f"Expected '{expected}', found '{ch}'")
            self.pos += 1
            return ch
        
        def skip_whitespace(self):
            """Skip whitespace characters."""
            while self.pos < self.length and self.text[self.pos] in ' \t\n\r':
                self.pos += 1
        
        def parse_value(self):
            """Parse a JSON value."""
            self.skip_whitespace()
            if self.pos >= self.length:
                raise ValueError("Unexpected end of input")
            
            ch = self.peek()
            if ch == '{':
                return self.parse_object()
            elif ch == '[':
                return self.parse_array()
            elif ch == '"':
                return self.parse_string()
            elif ch == 'n':
                return self.parse_null()
            elif ch == 't':
                return self.parse_true()
            elif ch == 'f':
                return self.parse_false()
            elif ch == '-' or ('0' <= ch <= '9'):
                return self.parse_number()
            else:
                raise ValueError(f"Unexpected character '{ch}'")
        
        def parse_object(self):
            """Parse a JSON object."""
            self.consume('{')
            self.skip_whitespace()
            
            obj = {}
            
            # Check for empty object
            if self.peek() == '}':
                self.consume('}')
                return obj
            
            while True:
                # Parse key
                self.skip_whitespace()
                key = self.parse_string()
                
                # Parse colon
                self.skip_whitespace()
                self.consume(':')
                
                # Parse value
                self.skip_whitespace()
                value = self.parse_value()
                
                # Add to object
                obj[key] = value
                
                # Check for comma or closing brace
                self.skip_whitespace()
                ch = self.peek()
                if ch == '}':
                    self.consume('}')
                    break
                elif ch == ',':
                    self.consume(',')
                    # Check for trailing comma
                    self.skip_whitespace()
                    if self.peek() == '}':
                        raise ValueError("Trailing comma in object")
                else:
                    raise ValueError(f"Expected ',' or '}}', found '{ch}'")
            
            return obj
        
        def parse_array(self):
            """Parse a JSON array."""
            self.consume('[')
            self.skip_whitespace()
            
            arr = []
            
            # Check for empty array
            if self.peek() == ']':
                self.consume(']')
                return arr
            
            while True:
                # Parse value
                self.skip_whitespace()
                value = self.parse_value()
                arr.append(value)
                
                # Check for comma or closing bracket
                self.skip_whitespace()
                ch = self.peek()
                if ch == ']':
                    self.consume(']')
                    break
                elif ch == ',':
                    self.consume(',')
                    # Check for trailing comma
                    self.skip_whitespace()
                    if self.peek() == ']':
                        raise ValueError("Trailing comma in array")
                else:
                    raise ValueError(f"Expected ',' or ']', found '{ch}'")
            
            return arr
        
        def parse_string(self):
            """Parse a JSON string."""
            self.consume('"')
            result = []
            
            while self.pos < self.length:
                ch = self.consume()
                if ch == '"':
                    return ''.join(result)
                elif ch == '\\':
                    # Escape sequence
                    if self.pos >= self.length:
                        raise ValueError("Incomplete escape sequence")
                    esc = self.consume()
                    if esc == '"':
                        result.append('"')
                    elif esc == '\\':
                        result.append('\\')
                    elif esc == '/':
                        result.append('/')
                    elif esc == 'b':
                        result.append('\b')
                    elif esc == 'f':
                        result.append('\f')
                    elif esc == 'n':
                        result.append('\n')
                    elif esc == 'r':
                        result.append('\r')
                    elif esc == 't':
                        result.append('\t')
                    elif esc == 'u':
                        # Unicode escape: \uXXXX
                        hex_digits = ''
                        for _ in range(4):
                            if self.pos >= self.length:
                                raise ValueError("Incomplete Unicode escape")
                            hex_ch = self.consume()
                            if not ('0' <= hex_ch <= '9' or 'a' <= hex_ch <= 'f' or 'A' <= hex_ch <= 'F'):
                                raise ValueError(f"Invalid hex digit in Unicode escape: '{hex_ch}'")
                            hex_digits += hex_ch
                        # Convert hex to Unicode character
                        try:
                            code_point = int(hex_digits, 16)
                            result.append(chr(code_point))
                        except ValueError:
                            raise ValueError(f"Invalid Unicode code point: \\u{hex_digits}")
                    else:
                        raise ValueError(f"Invalid escape sequence: \\{esc}")
                elif ord(ch) < 0x20:  # Control characters
                    raise ValueError(f"Control character in string: U+{ord(ch):04X}")
                else:
                    result.append(ch)
            
            raise ValueError("Unclosed string")
        
        def parse_null(self):
            """Parse the null literal."""
            self.consume('n')
            self.consume('u')
            self.consume('l')
            self.consume('l')
            return None
        
        def parse_true(self):
            """Parse the true literal."""
            self.consume('t')
            self.consume('r')
            self.consume('u')
            self.consume('e')
            return True
        
        def parse_false(self):
            """Parse the false literal."""
            self.consume('f')
            self.consume('a')
            self.consume('l')
            self.consume('s')
            self.consume('e')
            return False
        
        def parse_number(self):
            """Parse a JSON number."""
            start_pos = self.pos
            
            # Optional minus sign
            if self.peek() == '-':
                self.consume()
            
            # Integer part
            if self.peek() == '0':
                self.consume()
                # Check for leading zero (except 0 itself)
                if self.pos < self.length and '0' <= self.peek() <= '9':
                    raise ValueError("Number with leading zero")
            else:
                # At least one digit
                if self.pos >= self.length or not ('1' <= self.peek() <= '9'):
                    raise ValueError("Invalid number")
                while self.pos < self.length and '0' <= self.peek() <= '9':
                    self.consume()
            
            # Fraction part
            if self.pos < self.length and self.peek() == '.':
                self.consume()
                # At least one digit after decimal point
                if self.pos >= self.length or not ('0' <= self.peek() <= '9'):
                    raise ValueError("Invalid number: missing digits after decimal point")
                while self.pos < self.length and '0' <= self.peek() <= '9':
                    self.consume()
            
            # Exponent part
            if self.pos < self.length and self.peek() in 'eE':
                self.consume()
                # Optional sign
                if self.pos < self.length and self.peek() in '+-':
                    self.consume()
                # At least one digit
                if self.pos >= self.length or not ('0' <= self.peek() <= '9'):
                    raise ValueError("Invalid number: missing digits in exponent")
                while self.pos < self.length and '0' <= self.peek() <= '9':
                    self.consume()
            
            # Extract the number string and convert
            num_str = self.text[start_pos:self.pos]
            try:
                # Check if it's an integer or float
                if '.' in num_str or 'e' in num_str or 'E' in num_str:
                    return float(num_str)
                else:
                    return int(num_str)
            except ValueError:
                raise ValueError(f"Invalid number: {num_str}")
        
        def parse(self):
            """Parse the entire JSON document."""
            self.skip_whitespace()
            if self.pos >= self.length:
                raise ValueError("Empty input")
            
            result = self.parse_value()
            
            # Check for trailing content
            self.skip_whitespace()
            if self.pos < self.length:
                raise ValueError("Trailing content after JSON value")
            
            return result
    
    parser = Parser(text)
    return parser.parse()