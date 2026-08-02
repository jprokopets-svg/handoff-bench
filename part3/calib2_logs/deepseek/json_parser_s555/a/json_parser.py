def parse_json(text: str) -> object:
    """Parse a JSON string and return the corresponding Python object.
    
    Raises ValueError for any invalid JSON input.
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    
    # Use an index to track position in the string
    idx = 0
    n = len(text)
    
    def skip_whitespace():
        nonlocal idx
        while idx < n and text[idx] in ' \t\n\r':
            idx += 1
    
    def expect_end():
        skip_whitespace()
        if idx < n:
            raise ValueError("Trailing content after JSON value")
    
    def parse_value():
        skip_whitespace()
        if idx >= n:
            raise ValueError("Empty input or unexpected end")
        
        ch = text[idx]
        if ch == '{':
            return parse_object()
        elif ch == '[':
            return parse_array()
        elif ch == '"':
            return parse_string()
        elif ch == 'n':
            return parse_null()
        elif ch == 't':
            return parse_true()
        elif ch == 'f':
            return parse_false()
        elif ch == '-' or ch.isdigit():
            return parse_number()
        else:
            raise ValueError(f"Unexpected character '{ch}' at position {idx}")
    
    def parse_object():
        nonlocal idx
        if text[idx] != '{':
            raise ValueError("Expected '{'")
        idx += 1
        skip_whitespace()
        
        obj = {}
        first = True
        
        while idx < n and text[idx] != '}':
            if not first:
                skip_whitespace()
                if idx >= n or text[idx] != ',':
                    raise ValueError("Expected ',' between object items")
                idx += 1
                skip_whitespace()
            
            # Parse key (must be a string)
            if idx >= n or text[idx] != '"':
                raise ValueError("Object key must be a string")
            key = parse_string()
            
            skip_whitespace()
            if idx >= n or text[idx] != ':':
                raise ValueError("Expected ':' after object key")
            idx += 1
            skip_whitespace()
            
            # Parse value
            value = parse_value()
            obj[key] = value
            
            first = False
            skip_whitespace()
        
        if idx >= n or text[idx] != '}':
            raise ValueError("Unclosed object")
        idx += 1
        
        return obj
    
    def parse_array():
        nonlocal idx
        if text[idx] != '[':
            raise ValueError("Expected '['")
        idx += 1
        skip_whitespace()
        
        arr = []
        first = True
        
        while idx < n and text[idx] != ']':
            if not first:
                skip_whitespace()
                if idx >= n or text[idx] != ',':
                    raise ValueError("Expected ',' between array elements")
                idx += 1
                skip_whitespace()
            
            value = parse_value()
            arr.append(value)
            
            first = False
            skip_whitespace()
        
        if idx >= n or text[idx] != ']':
            raise ValueError("Unclosed array")
        idx += 1
        
        return arr
    
    def parse_string():
        nonlocal idx
        if text[idx] != '"':
            raise ValueError("Expected '\"'")
        idx += 1
        
        start = idx
        result_chars = []
        
        while idx < n and text[idx] != '"':
            ch = text[idx]
            if ch == '\\':
                idx += 1
                if idx >= n:
                    raise ValueError("Unterminated escape sequence")
                esc = text[idx]
                if esc == '"':
                    result_chars.append('"')
                elif esc == '\\':
                    result_chars.append('\\')
                elif esc == '/':
                    result_chars.append('/')
                elif esc == 'b':
                    result_chars.append('\b')
                elif esc == 'f':
                    result_chars.append('\f')
                elif esc == 'n':
                    result_chars.append('\n')
                elif esc == 'r':
                    result_chars.append('\r')
                elif esc == 't':
                    result_chars.append('\t')
                elif esc == 'u':
                    # Parse \uXXXX
                    if idx + 4 >= n:
                        raise ValueError("Incomplete Unicode escape")
                    hex_str = text[idx+1:idx+5]
                    try:
                        code_point = int(hex_str, 16)
                        # Convert to character
                        result_chars.append(chr(code_point))
                    except ValueError:
                        raise ValueError(f"Invalid Unicode escape: \\u{hex_str}")
                    idx += 4
                else:
                    raise ValueError(f"Invalid escape sequence: \\{esc}")
            elif ord(ch) < 32:  # Control characters
                raise ValueError(f"Control character in string: {repr(ch)}")
            else:
                result_chars.append(ch)
            idx += 1
        
        if idx >= n or text[idx] != '"':
            raise ValueError("Unclosed string")
        idx += 1
        
        return ''.join(result_chars)
    
    def parse_null():
        nonlocal idx
        if text[idx:idx+4] != 'null':
            raise ValueError("Expected 'null'")
        idx += 4
        return None
    
    def parse_true():
        nonlocal idx
        if text[idx:idx+4] != 'true':
            raise ValueError("Expected 'true'")
        idx += 4
        return True
    
    def parse_false():
        nonlocal idx
        if text[idx:idx+5] != 'false':
            raise ValueError("Expected 'false'")
        idx += 5
        return False
    
    def parse_number():
        nonlocal idx
        start = idx
        
        # Check for minus sign
        if text[idx] == '-':
            idx += 1
            if idx >= n or not text[idx].isdigit():
                raise ValueError("Invalid number format")
        
        # Parse integer part
        if idx < n and text[idx] == '0':
            idx += 1
            # Check for leading zero (not allowed unless it's just 0)
            if idx < n and text[idx].isdigit():
                raise ValueError("Numbers cannot have leading zeros")
        else:
            # Parse one or more digits
            if idx >= n or not text[idx].isdigit():
                raise ValueError("Invalid number format")
            while idx < n and text[idx].isdigit():
                idx += 1
        
        # Parse fraction part
        if idx < n and text[idx] == '.':
            idx += 1
            # Must have at least one digit after decimal point
            if idx >= n or not text[idx].isdigit():
                raise ValueError("Invalid number format")
            while idx < n and text[idx].isdigit():
                idx += 1
        
        # Parse exponent part
        if idx < n and text[idx] in 'eE':
            idx += 1
            # Optional sign
            if idx < n and text[idx] in '+-':
                idx += 1
            # Must have at least one digit
            if idx >= n or not text[idx].isdigit():
                raise ValueError("Invalid number format")
            while idx < n and text[idx].isdigit():
                idx += 1
        
        # Convert to float or int
        num_str = text[start:idx]
        try:
            # Check if it's an integer (no decimal point and no exponent)
            if '.' not in num_str and 'e' not in num_str and 'E' not in num_str:
                return int(num_str)
            else:
                return float(num_str)
        except ValueError:
            raise ValueError(f"Invalid number: {num_str}")
    
    # Main parsing
    if n == 0:
        raise ValueError("Empty input")
    
    skip_whitespace()
    if idx >= n:
        raise ValueError("Empty input")
    
    result = parse_value()
    expect_end()
    return result