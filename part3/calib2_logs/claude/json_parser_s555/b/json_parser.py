def parse_json(text: str) -> object:
    """
    Parse a JSON string and return the corresponding Python object.
    
    Supports: null, true, false, integers, floats, strings (with escapes),
    arrays, and objects. Rejects trailing content, unclosed structures,
    invalid escapes, leading zeros, and other JSON violations.
    
    Args:
        text: A JSON string to parse
        
    Returns:
        The parsed Python object (dict, list, str, int, float, bool, or None)
        
    Raises:
        ValueError: If the input is not valid JSON
        
    Examples:
        >>> parse_json('123')
        123
        >>> parse_json('{"a": 1}')
        {'a': 1}
        >>> parse_json('[1, 2, 3]')
        [1, 2, 3]
    """
    if not text:
        raise ValueError("Empty input")
    
    text = text.strip()
    if not text:
        raise ValueError("Empty input")
    
    value, pos = _parse_value(text, 0)
    
    # Check for trailing content
    pos = _skip_whitespace(text, pos)
    if pos < len(text):
        raise ValueError(f"Trailing content after JSON value at position {pos}")
    
    return value


def _skip_whitespace(text: str, pos: int) -> int:
    """Skip whitespace characters and return new position."""
    while pos < len(text) and text[pos] in ' \t\n\r':
        pos += 1
    return pos


def _parse_value(text: str, pos: int) -> tuple:
    """Parse a JSON value and return (value, new_position)."""
    pos = _skip_whitespace(text, pos)
    
    if pos >= len(text):
        raise ValueError("Unexpected end of input")
    
    char = text[pos]
    
    if char == 'n':
        return _parse_null(text, pos)
    elif char == 't':
        return _parse_true(text, pos)
    elif char == 'f':
        return _parse_false(text, pos)
    elif char == '"':
        return _parse_string(text, pos)
    elif char == '[':
        return _parse_array(text, pos)
    elif char == '{':
        return _parse_object(text, pos)
    elif char == '-' or char.isdigit():
        return _parse_number(text, pos)
    else:
        raise ValueError(f"Unexpected character '{char}' at position {pos}")


def _parse_null(text: str, pos: int) -> tuple:
    """Parse null literal."""
    if text[pos:pos+4] == 'null':
        return None, pos + 4
    raise ValueError(f"Invalid literal at position {pos}")


def _parse_true(text: str, pos: int) -> tuple:
    """Parse true literal."""
    if text[pos:pos+4] == 'true':
        return True, pos + 4
    raise ValueError(f"Invalid literal at position {pos}")


def _parse_false(text: str, pos: int) -> tuple:
    """Parse false literal."""
    if text[pos:pos+5] == 'false':
        return False, pos + 5
    raise ValueError(f"Invalid literal at position {pos}")


def _parse_string(text: str, pos: int) -> tuple:
    """Parse a JSON string with escape sequences."""
    if text[pos] != '"':
        raise ValueError(f"Expected '\"' at position {pos}")
    
    pos += 1
    result = []
    
    while pos < len(text):
        char = text[pos]
        
        if char == '"':
            return ''.join(result), pos + 1
        elif char == '\\':
            if pos + 1 >= len(text):
                raise ValueError("Unclosed string: unexpected end of input")
            
            next_char = text[pos + 1]
            if next_char == '"':
                result.append('"')
                pos += 2
            elif next_char == '\\':
                result.append('\\')
                pos += 2
            elif next_char == '/':
                result.append('/')
                pos += 2
            elif next_char == 'b':
                result.append('\b')
                pos += 2
            elif next_char == 'f':
                result.append('\f')
                pos += 2
            elif next_char == 'n':
                result.append('\n')
                pos += 2
            elif next_char == 'r':
                result.append('\r')
                pos += 2
            elif next_char == 't':
                result.append('\t')
                pos += 2
            elif next_char == 'u':
                if pos + 6 > len(text):
                    raise ValueError("Invalid unicode escape: not enough characters")
                hex_digits = text[pos+2:pos+6]
                if len(hex_digits) != 4 or not all(c in '0123456789abcdefABCDEF' for c in hex_digits):
                    raise ValueError(f"Invalid unicode escape sequence at position {pos}")
                code_point = int(hex_digits, 16)
                result.append(chr(code_point))
                pos += 6
            else:
                raise ValueError(f"Invalid escape sequence '\\{next_char}' at position {pos}")
        elif ord(char) < 0x20:
            raise ValueError(f"Control character in string at position {pos}")
        else:
            result.append(char)
            pos += 1
    
    raise ValueError("Unclosed string")


def _parse_number(text: str, pos: int) -> tuple:
    """Parse a JSON number (integer or float)."""
    start = pos
    
    # Optional minus sign
    if pos < len(text) and text[pos] == '-':
        pos += 1
    
    if pos >= len(text) or not text[pos].isdigit():
        raise ValueError(f"Invalid number at position {start}")
    
    # Integer part
    if text[pos] == '0':
        pos += 1
        # Leading zero is only allowed if it's just "0"
        if pos < len(text) and text[pos].isdigit():
            raise ValueError(f"Leading zero in number at position {start}")
    else:
        while pos < len(text) and text[pos].isdigit():
            pos += 1
    
    is_float = False
    
    # Fractional part
    if pos < len(text) and text[pos] == '.':
        is_float = True
        pos += 1
        if pos >= len(text) or not text[pos].isdigit():
            raise ValueError(f"Invalid number: expected digit after decimal point at position {pos}")
        while pos < len(text) and text[pos].isdigit():
            pos += 1
    
    # Exponent part
    if pos < len(text) and text[pos] in 'eE':
        is_float = True
        pos += 1
        if pos < len(text) and text[pos] in '+-':
            pos += 1
        if pos >= len(text) or not text[pos].isdigit():
            raise ValueError(f"Invalid number: expected digit in exponent at position {pos}")
        while pos < len(text) and text[pos].isdigit():
            pos += 1
    
    number_str = text[start:pos]
    try:
        if is_float:
            value = float(number_str)
        else:
            value = int(number_str)
    except ValueError:
        raise ValueError(f"Invalid number at position {start}")
    
    return value, pos


def _parse_array(text: str, pos: int) -> tuple:
    """Parse a JSON array."""
    if text[pos] != '[':
        raise ValueError(f"Expected '[' at position {pos}")
    
    pos += 1
    pos = _skip_whitespace(text, pos)
    
    result = []
    
    # Empty array
    if pos < len(text) and text[pos] == ']':
        return result, pos + 1
    
    while True:
        value, pos = _parse_value(text, pos)
        result.append(value)
        
        pos = _skip_whitespace(text, pos)
        
        if pos >= len(text):
            raise ValueError("Unclosed array")
        
        if text[pos] == ']':
            return result, pos + 1
        elif text[pos] == ',':
            pos += 1
            pos = _skip_whitespace(text, pos)
            # Check for trailing comma
            if pos < len(text) and text[pos] == ']':
                raise ValueError("Trailing comma in array")
        else:
            raise ValueError(f"Expected ',' or ']' in array at position {pos}")


def _parse_object(text: str, pos: int) -> tuple:
    """Parse a JSON object."""
    if text[pos] != '{':
        raise ValueError(f"Expected '{{' at position {pos}")
    
    pos += 1
    pos = _skip_whitespace(text, pos)
    
    result = {}
    
    # Empty object
    if pos < len(text) and text[pos] == '}':
        return result, pos + 1
    
    while True:
        pos = _skip_whitespace(text, pos)
        
        if pos >= len(text):
            raise ValueError("Unclosed object")
        
        # Key must be a string
        if text[pos] != '"':
            raise ValueError(f"Expected string key in object at position {pos}")
        
        key, pos = _parse_string(text, pos)
        
        pos = _skip_whitespace(text, pos)
        
        if pos >= len(text) or text[pos] != ':':
            raise ValueError(f"Expected ':' after key in object at position {pos}")
        
        pos += 1
        
        value, pos = _parse_value(text, pos)
        result[key] = value
        
        pos = _skip_whitespace(text, pos)
        
        if pos >= len(text):
            raise ValueError("Unclosed object")
        
        if text[pos] == '}':
            return result, pos + 1
        elif text[pos] == ',':
            pos += 1
            pos = _skip_whitespace(text, pos)
            # Check for trailing comma
            if pos < len(text) and text[pos] == '}':
                raise ValueError("Trailing comma in object")
        else:
            raise ValueError(f"Expected ',' or '}}' in object at position {pos}")
