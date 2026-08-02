def parse_json(text):
    """
    Parse a single JSON value from text and return the Python equivalent.
    Raises ValueError on any invalid input.
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string")
    
    # Strip leading whitespace
    pos = 0
    while pos < len(text) and text[pos] in ' \t\n\r':
        pos += 1
    
    if pos >= len(text):
        raise ValueError("Empty input")
    
    # Parse the value
    value, pos = _parse_value(text, pos)
    
    # Strip trailing whitespace
    while pos < len(text) and text[pos] in ' \t\n\r':
        pos += 1
    
    # Check for trailing content
    if pos < len(text):
        raise ValueError("Trailing content after JSON value")
    
    return value


def _parse_value(text, pos):
    """Parse a JSON value starting at position pos. Returns (value, new_pos)."""
    # Skip whitespace
    while pos < len(text) and text[pos] in ' \t\n\r':
        pos += 1
    
    if pos >= len(text):
        raise ValueError("Unexpected end of input")
    
    ch = text[pos]
    
    if ch == 'n':
        return _parse_null(text, pos)
    elif ch == 't':
        return _parse_true(text, pos)
    elif ch == 'f':
        return _parse_false(text, pos)
    elif ch == '"':
        return _parse_string(text, pos)
    elif ch == '[':
        return _parse_array(text, pos)
    elif ch == '{':
        return _parse_object(text, pos)
    elif ch == '-' or ch.isdigit():
        return _parse_number(text, pos)
    else:
        raise ValueError(f"Unexpected character: {ch}")


def _parse_null(text, pos):
    """Parse null literal."""
    if text[pos:pos+4] == 'null':
        return None, pos + 4
    raise ValueError("Invalid null literal")


def _parse_true(text, pos):
    """Parse true literal."""
    if text[pos:pos+4] == 'true':
        return True, pos + 4
    raise ValueError("Invalid true literal")


def _parse_false(text, pos):
    """Parse false literal."""
    if text[pos:pos+5] == 'false':
        return False, pos + 5
    raise ValueError("Invalid false literal")


def _parse_string(text, pos):
    """Parse a JSON string starting at pos (which should be at the opening quote)."""
    if text[pos] != '"':
        raise ValueError("String must start with quote")
    
    pos += 1
    result = []
    
    while pos < len(text):
        ch = text[pos]
        
        if ch == '"':
            return ''.join(result), pos + 1
        elif ch == '\\':
            if pos + 1 >= len(text):
                raise ValueError("Unclosed string")
            
            next_ch = text[pos + 1]
            if next_ch == '"':
                result.append('"')
                pos += 2
            elif next_ch == '\\':
                result.append('\\')
                pos += 2
            elif next_ch == '/':
                result.append('/')
                pos += 2
            elif next_ch == 'b':
                result.append('\b')
                pos += 2
            elif next_ch == 'f':
                result.append('\f')
                pos += 2
            elif next_ch == 'n':
                result.append('\n')
                pos += 2
            elif next_ch == 'r':
                result.append('\r')
                pos += 2
            elif next_ch == 't':
                result.append('\t')
                pos += 2
            elif next_ch == 'u':
                # Unicode escape: \uXXXX (exactly 4 hex digits)
                if pos + 6 > len(text):
                    raise ValueError("Invalid unicode escape")
                hex_str = text[pos+2:pos+6]
                if len(hex_str) != 4 or not all(c in '0123456789abcdefABCDEF' for c in hex_str):
                    raise ValueError("Invalid unicode escape")
                code_point = int(hex_str, 16)
                result.append(chr(code_point))
                pos += 6
            else:
                raise ValueError(f"Invalid escape sequence: \\{next_ch}")
        elif ord(ch) < 0x20:
            # Control characters are not allowed in strings
            raise ValueError("Control character in string")
        else:
            result.append(ch)
            pos += 1
    
    raise ValueError("Unclosed string")


def _parse_number(text, pos):
    """Parse a JSON number starting at pos."""
    start = pos
    
    # Optional minus sign
    if pos < len(text) and text[pos] == '-':
        pos += 1
    
    if pos >= len(text):
        raise ValueError("Invalid number")
    
    # Integer part
    if text[pos] == '0':
        pos += 1
        # Leading zeros are not allowed (except for just "0")
        if pos < len(text) and text[pos].isdigit():
            raise ValueError("Leading zeros not allowed")
    elif text[pos].isdigit():
        while pos < len(text) and text[pos].isdigit():
            pos += 1
    else:
        raise ValueError("Invalid number")
    
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
            raise ValueError("Invalid number: exponent must be followed by digits")
        
        if text[pos] in '+-':
            pos += 1
        
        if pos >= len(text) or not text[pos].isdigit():
            raise ValueError("Invalid number: exponent must be followed by digits")
        
        while pos < len(text) and text[pos].isdigit():
            pos += 1
    
    number_str = text[start:pos]
    
    try:
        # Try to parse as int first
        if '.' not in number_str and 'e' not in number_str and 'E' not in number_str:
            return int(number_str), pos
        else:
            return float(number_str), pos
    except ValueError:
        raise ValueError(f"Invalid number: {number_str}")


def _parse_array(text, pos):
    """Parse a JSON array starting at pos (which should be at the opening bracket)."""
    if text[pos] != '[':
        raise ValueError("Array must start with [")
    
    pos += 1
    result = []
    
    # Skip whitespace
    while pos < len(text) and text[pos] in ' \t\n\r':
        pos += 1
    
    # Empty array
    if pos < len(text) and text[pos] == ']':
        return result, pos + 1
    
    while True:
        # Parse value
        value, pos = _parse_value(text, pos)
        result.append(value)
        
        # Skip whitespace
        while pos < len(text) and text[pos] in ' \t\n\r':
            pos += 1
        
        if pos >= len(text):
            raise ValueError("Unclosed array")
        
        if text[pos] == ']':
            return result, pos + 1
        elif text[pos] == ',':
            pos += 1
            # Skip whitespace after comma
            while pos < len(text) and text[pos] in ' \t\n\r':
                pos += 1
            
            # Check for trailing comma
            if pos < len(text) and text[pos] == ']':
                raise ValueError("Trailing comma in array")
        else:
            raise ValueError(f"Expected ',' or ']' in array, got {text[pos]}")


def _parse_object(text, pos):
    """Parse a JSON object starting at pos (which should be at the opening brace)."""
    if text[pos] != '{':
        raise ValueError("Object must start with {")
    
    pos += 1
    result = {}
    
    # Skip whitespace
    while pos < len(text) and text[pos] in ' \t\n\r':
        pos += 1
    
    # Empty object
    if pos < len(text) and text[pos] == '}':
        return result, pos + 1
    
    while True:
        # Skip whitespace
        while pos < len(text) and text[pos] in ' \t\n\r':
            pos += 1
        
        if pos >= len(text):
            raise ValueError("Unclosed object")
        
        # Parse key (must be a string)
        if text[pos] != '"':
            raise ValueError("Object key must be a string")
        
        key, pos = _parse_string(text, pos)
        
        # Skip whitespace
        while pos < len(text) and text[pos] in ' \t\n\r':
            pos += 1
        
        if pos >= len(text) or text[pos] != ':':
            raise ValueError("Expected ':' after object key")
        
        pos += 1
        
        # Parse value
        value, pos = _parse_value(text, pos)
        result[key] = value
        
        # Skip whitespace
        while pos < len(text) and text[pos] in ' \t\n\r':
            pos += 1
        
        if pos >= len(text):
            raise ValueError("Unclosed object")
        
        if text[pos] == '}':
            return result, pos + 1
        elif text[pos] == ',':
            pos += 1
            # Skip whitespace after comma
            while pos < len(text) and text[pos] in ' \t\n\r':
                pos += 1
            
            # Check for trailing comma
            if pos < len(text) and text[pos] == '}':
                raise ValueError("Trailing comma in object")
        else:
            raise ValueError(f"Expected ',' or '}}' in object, got {text[pos]}")
