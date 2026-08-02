def parse_json(text: str) -> object:
    """Parse a JSON string and return the Python equivalent."""
    if not text:
        raise ValueError("Empty input")
    
    parser = JSONParser(text)
    value = parser.parse_value()
    parser.skip_whitespace()
    
    # Check for trailing content
    if parser.pos < len(parser.text):
        raise ValueError("Trailing content after JSON value")
    
    return value


class JSONParser:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
    
    def skip_whitespace(self):
        """Skip whitespace characters."""
        while self.pos < len(self.text) and self.text[self.pos] in ' \t\n\r':
            self.pos += 1
    
    def peek(self):
        """Peek at the current character without consuming it."""
        self.skip_whitespace()
        if self.pos < len(self.text):
            return self.text[self.pos]
        return None
    
    def consume(self, expected=None):
        """Consume and return the current character."""
        self.skip_whitespace()
        if self.pos >= len(self.text):
            raise ValueError("Unexpected end of input")
        char = self.text[self.pos]
        if expected and char != expected:
            raise ValueError(f"Expected '{expected}', got '{char}'")
        self.pos += 1
        return char
    
    def parse_value(self):
        """Parse a JSON value (dispatcher)."""
        char = self.peek()
        
        if char is None:
            raise ValueError("Unexpected end of input")
        elif char == 'n':
            return self.parse_null()
        elif char == 't':
            return self.parse_true()
        elif char == 'f':
            return self.parse_false()
        elif char == '"':
            return self.parse_string()
        elif char == '[':
            return self.parse_array()
        elif char == '{':
            return self.parse_object()
        elif char == '-' or char.isdigit():
            return self.parse_number()
        else:
            raise ValueError(f"Unexpected character: '{char}'")
    
    def parse_null(self):
        """Parse null."""
        self.consume('n')
        self.consume('u')
        self.consume('l')
        self.consume('l')
        return None
    
    def parse_true(self):
        """Parse true."""
        self.consume('t')
        self.consume('r')
        self.consume('u')
        self.consume('e')
        return True
    
    def parse_false(self):
        """Parse false."""
        self.consume('f')
        self.consume('a')
        self.consume('l')
        self.consume('s')
        self.consume('e')
        return False
    
    def parse_string(self):
        """Parse a JSON string with escape sequences."""
        self.consume('"')
        result = []
        
        while self.pos < len(self.text):
            char = self.text[self.pos]
            
            if char == '"':
                self.pos += 1
                return ''.join(result)
            elif char == '\\':
                self.pos += 1
                if self.pos >= len(self.text):
                    raise ValueError("Unclosed string")
                escape_char = self.text[self.pos]
                
                if escape_char == '"':
                    result.append('"')
                elif escape_char == '\\':
                    result.append('\\')
                elif escape_char == '/':
                    result.append('/')
                elif escape_char == 'b':
                    result.append('\b')
                elif escape_char == 'f':
                    result.append('\f')
                elif escape_char == 'n':
                    result.append('\n')
                elif escape_char == 'r':
                    result.append('\r')
                elif escape_char == 't':
                    result.append('\t')
                elif escape_char == 'u':
                    # Unicode escape: \uXXXX
                    self.pos += 1
                    if self.pos + 3 >= len(self.text):
                        raise ValueError("Invalid unicode escape")
                    hex_digits = self.text[self.pos:self.pos + 4]
                    if len(hex_digits) != 4 or not all(c in '0123456789abcdefABCDEF' for c in hex_digits):
                        raise ValueError("Invalid unicode escape")
                    code_point = int(hex_digits, 16)
                    result.append(chr(code_point))
                    self.pos += 3
                else:
                    raise ValueError(f"Invalid escape sequence: \\{escape_char}")
                
                self.pos += 1
            elif ord(char) < 0x20:
                # Control characters are not allowed in strings
                raise ValueError("Control character in string")
            else:
                result.append(char)
                self.pos += 1
        
        raise ValueError("Unclosed string")
    
    def parse_number(self):
        """Parse a JSON number (integer or float with optional exponent)."""
        start = self.pos
        
        # Optional minus sign
        if self.pos < len(self.text) and self.text[self.pos] == '-':
            self.pos += 1
        
        # Integer part
        if self.pos >= len(self.text) or not self.text[self.pos].isdigit():
            raise ValueError("Invalid number")
        
        # Check for leading zero
        if self.text[self.pos] == '0':
            self.pos += 1
            # After a leading 0, we must have . or e/E or end
            if self.pos < len(self.text) and self.text[self.pos].isdigit():
                raise ValueError("Leading zeros not allowed")
        else:
            # Consume remaining digits
            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                self.pos += 1
        
        # Optional fraction part
        if self.pos < len(self.text) and self.text[self.pos] == '.':
            self.pos += 1
            if self.pos >= len(self.text) or not self.text[self.pos].isdigit():
                raise ValueError("Invalid number: decimal point must be followed by digits")
            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                self.pos += 1
        
        # Optional exponent part
        if self.pos < len(self.text) and self.text[self.pos] in 'eE':
            self.pos += 1
            if self.pos >= len(self.text):
                raise ValueError("Invalid number: exponent must have digits")
            
            # Optional sign in exponent
            if self.text[self.pos] in '+-':
                self.pos += 1
            
            if self.pos >= len(self.text) or not self.text[self.pos].isdigit():
                raise ValueError("Invalid number: exponent must have digits")
            
            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                self.pos += 1
        
        number_str = self.text[start:self.pos]
        
        # Parse the number
        if '.' in number_str or 'e' in number_str or 'E' in number_str:
            return float(number_str)
        else:
            return int(number_str)
    
    def parse_array(self):
        """Parse a JSON array."""
        self.consume('[')
        result = []
        
        # Check for empty array
        if self.peek() == ']':
            self.consume(']')
            return result
        
        while True:
            result.append(self.parse_value())
            
            char = self.peek()
            if char == ']':
                self.consume(']')
                return result
            elif char == ',':
                self.consume(',')
                # Check for trailing comma
                if self.peek() == ']':
                    raise ValueError("Trailing comma in array")
            else:
                raise ValueError("Expected ',' or ']' in array")
    
    def parse_object(self):
        """Parse a JSON object."""
        self.consume('{')
        result = {}
        
        # Check for empty object
        if self.peek() == '}':
            self.consume('}')
            return result
        
        while True:
            # Parse key (must be a string)
            if self.peek() != '"':
                raise ValueError("Object key must be a string")
            key = self.parse_string()
            
            # Parse colon
            self.consume(':')
            
            # Parse value
            value = self.parse_value()
            result[key] = value
            
            char = self.peek()
            if char == '}':
                self.consume('}')
                return result
            elif char == ',':
                self.consume(',')
                # Check for trailing comma
                if self.peek() == '}':
                    raise ValueError("Trailing comma in object")
            else:
                raise ValueError("Expected ',' or '}' in object")
