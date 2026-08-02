def parse_json(text):
    """
    Parse a JSON string and return the Python equivalent.
    Raises ValueError on invalid input.
    """
    if not text:
        raise ValueError("Empty input")
    
    # Strip leading whitespace and parse
    pos = 0
    pos = skip_whitespace(text, pos)
    
    if pos >= len(text):
        raise ValueError("Empty input")
    
    value, pos = parse_value(text, pos)
    
    # Skip trailing whitespace
    pos = skip_whitespace(text, pos)
    
    # Check for trailing content
    if pos < len(text):
        raise ValueError("Trailing content after JSON value")
    
    return value


def skip_whitespace(text, pos):
    """Skip whitespace characters and return new position."""
    while pos < len(text) and text[pos] in ' \t\n\r':
        pos += 1
    return pos


def parse_value(text, pos):
    """Parse a JSON value and return (value, new_position)."""
    pos = skip_whitespace(text, pos)
    
    if pos >= len(text):
        raise ValueError("Unexpected end of input")
    
    char = text[pos]
    
    if char == 'n':
        return parse_null(text, pos)
    elif char == 't':
        return parse_true(text, pos)
    elif char == 'f':
        return parse_false(text, pos)
    elif char == '"':
        return parse_string(text, pos)
    elif char == '[':
        return parse_array(text, pos)
    elif char == '{':
        return parse_object(text, pos)
    elif char == '-' or char.isdigit():
        return parse_number(text, pos)
    else:
        raise ValueError(f"Unexpected character: {char}")


def parse_null(text, pos):
    """Parse null literal."""
    if text[pos:pos+4] == 'null':
        return None, pos + 4
    raise ValueError("Invalid null")


def parse_true(text, pos):
    """Parse true literal."""
    if text[pos:pos+4] == 'true':
        return True, pos + 4
    raise ValueError("Invalid true")


def parse_false(text, pos):
    """Parse false literal."""
    if text[pos:pos+5] == 'false':
        return False, pos + 5
    raise ValueError("Invalid false")


def parse_string(text, pos):
    """Parse a JSON string and return (string_value, new_position)."""
    if text[pos] != '"':
        raise ValueError("String must start with quote")
    
    pos += 1
    result = []
    
    while pos < len(text):
        char = text[pos]
        
        if char == '"':
            return ''.join(result), pos + 1
        elif char == '\\':
            pos += 1
            if pos >= len(text):
                raise ValueError("Unclosed string")
            
            escape_char = text[pos]
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
                # Unicode escape: \uXXXX (exactly 4 hex digits)
                pos += 1
                if pos + 3 >= len(text):
                    raise ValueError("Invalid unicode escape")
                hex_str = text[pos:pos+4]
                if len(hex_str) != 4 or not all(c in '0123456789abcdefABCDEF' for c in hex_str):
                    raise ValueError("Invalid unicode escape")
                code_point = int(hex_str, 16)
                result.append(chr(code_point))
                pos += 3
            else:
                raise ValueError(f"Invalid escape sequence: \\{escape_char}")
            pos += 1
        elif ord(char) < 0x20:
            # Control characters are not allowed in strings
            raise ValueError("Control character in string")
        else:
            result.append(char)
            pos += 1
    
    raise ValueError("Unclosed string")


def parse_number(text, pos):
    """Parse a JSON number and return (number_value, new_position)."""
    start = pos
    
    # Optional minus sign
    if pos < len(text) and text[pos] == '-':
        pos += 1
    else:
        # No plus sign allowed
        pass
    
    if pos >= len(text) or not text[pos].isdigit():
        raise ValueError("Invalid number")
    
    # Integer part
    if text[pos] == '0':
        pos += 1
        # Leading zeros not allowed (e.g., 01 is invalid)
        if pos < len(text) and text[pos].isdigit():
            raise ValueError("Leading zeros not allowed")
    else:
        while pos < len(text) and text[pos].isdigit():
            pos += 1
    
    # Optional fraction part
    if pos < len(text) and text[pos] == '.':
        pos += 1
        if pos >= len(text) or not text[pos].isdigit():
            raise ValueError("Invalid number: decimal point must be followed by digits")
        while pos < len(text) and text[pos].isdigit():
            pos += 1
    
    # Optional exponent part
    if pos < len(text) and text[pos] in 'eE':
        pos += 1
        if pos >= len(text):
            raise ValueError("Invalid number: exponent incomplete")
        
        if text[pos] in '+-':
            pos += 1
        
        if pos >= len(text) or not text[pos].isdigit():
            raise ValueError("Invalid number: exponent must have digits")
        
        while pos < len(text) and text[pos].isdigit():
            pos += 1
    
    number_str = text[start:pos]
    try:
        # Try to parse as int first, then float
        if '.' in number_str or 'e' in number_str or 'E' in number_str:
            return float(number_str), pos
        else:
            return int(number_str), pos
    except ValueError:
        raise ValueError(f"Invalid number: {number_str}")


def parse_array(text, pos):
    """Parse a JSON array and return (array_value, new_position)."""
    if text[pos] != '[':
        raise ValueError("Array must start with [")
    
    pos += 1
    result = []
    
    pos = skip_whitespace(text, pos)
    
    # Empty array
    if pos < len(text) and text[pos] == ']':
        return result, pos + 1
    
    while True:
        value, pos = parse_value(text, pos)
        result.append(value)
        
        pos = skip_whitespace(text, pos)
        
        if pos >= len(text):
            raise ValueError("Unclosed array")
        
        if text[pos] == ']':
            return result, pos + 1
        elif text[pos] == ',':
            pos += 1
            pos = skip_whitespace(text, pos)
            
            # Check for trailing comma
            if pos < len(text) and text[pos] == ']':
                raise ValueError("Trailing comma in array")
        else:
            raise ValueError(f"Expected ',' or ']' in array, got {text[pos]}")


def parse_object(text, pos):
    """Parse a JSON object and return (object_value, new_position)."""
    if text[pos] != '{':
        raise ValueError("Object must start with {")
    
    pos += 1
    result = {}
    
    pos = skip_whitespace(text, pos)
    
    # Empty object
    if pos < len(text) and text[pos] == '}':
        return result, pos + 1
    
    while True:
        pos = skip_whitespace(text, pos)
        
        if pos >= len(text):
            raise ValueError("Unclosed object")
        
        # Key must be a string
        if text[pos] != '"':
            raise ValueError("Object key must be a string")
        
        key, pos = parse_string(text, pos)
        
        pos = skip_whitespace(text, pos)
        
        if pos >= len(text) or text[pos] != ':':
            raise ValueError("Expected ':' after object key")
        
        pos += 1
        
        value, pos = parse_value(text, pos)
        result[key] = value
        
        pos = skip_whitespace(text, pos)
        
        if pos >= len(text):
            raise ValueError("Unclosed object")
        
        if text[pos] == '}':
            return result, pos + 1
        elif text[pos] == ',':
            pos += 1
            pos = skip_whitespace(text, pos)
            
            # Check for trailing comma
            if pos < len(text) and text[pos] == '}':
                raise ValueError("Trailing comma in object")
        else:
            raise ValueError(f"Expected ',' or '}}' in object, got {text[pos]}")
