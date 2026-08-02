import re
from typing import Union, Dict, List

def parse_json(text: str) -> Union[Dict, List, str, int, float, bool, None]:
    """
    Parse a JSON string and return the Python equivalent.
    Raises ValueError on invalid input.
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string")
    
    text = text.strip()
    if not text:
        raise ValueError("Empty input")
    
    # Parse the JSON value and check for trailing content
    result, idx = _parse_value(text, 0)
    
    # Check for trailing content
    idx = _skip_whitespace(text, idx)
    if idx != len(text):
        raise ValueError("Trailing content after JSON value")
    
    return result


def _skip_whitespace(text: str, idx: int) -> int:
    """Skip whitespace characters."""
    while idx < len(text) and text[idx] in ' \t\n\r':
        idx += 1
    return idx


def _parse_value(text: str, idx: int) -> tuple:
    """Parse a JSON value starting at idx."""
    idx = _skip_whitespace(text, idx)
    
    if idx >= len(text):
        raise ValueError("Unexpected end of input")
    
    ch = text[idx]
    
    if ch == '{':
        return _parse_object(text, idx)
    elif ch == '[':
        return _parse_array(text, idx)
    elif ch == '"':
        return _parse_string(text, idx)
    elif ch == 't':
        return _parse_true(text, idx)
    elif ch == 'f':
        return _parse_false(text, idx)
    elif ch == 'n':
        return _parse_null(text, idx)
    elif ch == '-' or ch.isdigit():
        return _parse_number(text, idx)
    else:
        raise ValueError(f"Unexpected character '{ch}' at position {idx}")


def _parse_object(text: str, idx: int) -> tuple:
    """Parse a JSON object."""
    if text[idx] != '{':
        raise ValueError(f"Expected '{{' at position {idx}")
    
    idx += 1
    idx = _skip_whitespace(text, idx)
    obj = {}
    
    if idx < len(text) and text[idx] == '}':
        # Empty object
        return obj, idx + 1
    
    first = True
    while True:
        if not first:
            idx = _skip_whitespace(text, idx)
            if idx >= len(text):
                raise ValueError("Unclosed object")
            if text[idx] != ',':
                break
            idx += 1
            idx = _skip_whitespace(text, idx)
        
        # Parse key
        if idx >= len(text) or text[idx] != '"':
            raise ValueError(f"Expected string key at position {idx}")
        key, idx = _parse_string(text, idx)
        
        # Parse colon
        idx = _skip_whitespace(text, idx)
        if idx >= len(text) or text[idx] != ':':
            raise ValueError(f"Expected ':' at position {idx}")
        idx += 1
        
        # Parse value
        value, idx = _parse_value(text, idx)
        obj[key] = value
        
        first = False
    
    idx = _skip_whitespace(text, idx)
    if idx >= len(text) or text[idx] != '}':
        raise ValueError("Unclosed object")
    
    return obj, idx + 1


def _parse_array(text: str, idx: int) -> tuple:
    """Parse a JSON array."""
    if text[idx] != '[':
        raise ValueError(f"Expected '[' at position {idx}")
    
    idx += 1
    idx = _skip_whitespace(text, idx)
    arr = []
    
    if idx < len(text) and text[idx] == ']':
        # Empty array
        return arr, idx + 1
    
    first = True
    while True:
        if not first:
            idx = _skip_whitespace(text, idx)
            if idx >= len(text):
                raise ValueError("Unclosed array")
            if text[idx] != ',':
                break
            idx += 1
            idx = _skip_whitespace(text, idx)
        
        # Parse value
        value, idx = _parse_value(text, idx)
        arr.append(value)
        
        first = False
    
    idx = _skip_whitespace(text, idx)
    if idx >= len(text) or text[idx] != ']':
        raise ValueError("Unclosed array")
    
    return arr, idx + 1


def _parse_string(text: str, idx: int) -> tuple:
    """Parse a JSON string."""
    if text[idx] != '"':
        raise ValueError(f"Expected '\"' at position {idx}")
    
    idx += 1
    start = idx
    result = []
    
    while idx < len(text):
        ch = text[idx]
        
        if ch == '"':
            # End of string
            if start < idx:
                result.append(text[start:idx])
            idx += 1
            return ''.join(result), idx
        
        elif ch == '\\':
            # Escape sequence
            if start < idx:
                result.append(text[start:idx])
            
            idx += 1
            if idx >= len(text):
                raise ValueError("Unterminated escape sequence")
            
            esc = text[idx]
            idx += 1
            
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
                # Unicode escape
                if idx + 4 > len(text):
                    raise ValueError("Incomplete Unicode escape")
                
                hex_str = text[idx:idx+4]
                if not all(c in '0123456789abcdefABCDEF' for c in hex_str):
                    raise ValueError(f"Invalid Unicode escape: \\u{hex_str}")
                
                code_point = int(hex_str, 16)
                result.append(chr(code_point))
                idx += 4
            else:
                raise ValueError(f"Invalid escape sequence: \\{esc}")
            
            start = idx
        
        elif ord(ch) < 0x20:
            # Control characters (except whitespace which we skip earlier)
            raise ValueError(f"Control character in string at position {idx}")
        
        else:
            idx += 1
    
    raise ValueError("Unclosed string")


def _parse_true(text: str, idx: int) -> tuple:
    """Parse 'true' literal."""
    if text[idx:idx+4] == 'true':
        return True, idx + 4
    raise ValueError(f"Expected 'true' at position {idx}")


def _parse_false(text: str, idx: int) -> tuple:
    """Parse 'false' literal."""
    if text[idx:idx+5] == 'false':
        return False, idx + 5
    raise ValueError(f"Expected 'false' at position {idx}")


def _parse_null(text: str, idx: int) -> tuple:
    """Parse 'null' literal."""
    if text[idx:idx+4] == 'null':
        return None, idx + 4
    raise ValueError(f"Expected 'null' at position {idx}")


def _parse_number(text: str, idx: int) -> tuple:
    """Parse a JSON number."""
    start = idx
    
    # Check for leading zero
    if text[idx] == '0' and idx + 1 < len(text) and text[idx+1].isdigit():
        raise ValueError("Numbers cannot have leading zeros")
    
    # Optional minus sign
    if text[idx] == '-':
        idx += 1
        if idx >= len(text):
            raise ValueError("Incomplete number")
    
    # Integer part
    if idx < len(text) and text[idx] == '0':
        idx += 1
    elif idx < len(text) and text[idx].isdigit():
        while idx < len(text) and text[idx].isdigit():
            idx += 1
    else:
        raise ValueError(f"Expected digit at position {idx}")
    
    # Fraction part
    if idx < len(text) and text[idx] == '.':
        idx += 1
        if idx >= len(text) or not text[idx].isdigit():
            raise ValueError("Expected digit after decimal point")
        
        while idx < len(text) and text[idx].isdigit():
            idx += 1
    
    # Exponent part
    if idx < len(text) and text[idx] in 'eE':
        idx += 1
        if idx >= len(text):
            raise ValueError("Incomplete exponent")
        
        if text[idx] in '+-':
            idx += 1
        
        if idx >= len(text) or not text[idx].isdigit():
            raise ValueError("Expected digit in exponent")
        
        while idx < len(text) and text[idx].isdigit():
            idx += 1
    
    # Parse the number
    num_str = text[start:idx]
    
    # Check for invalid formats
    if num_str.startswith('+'):
        raise ValueError("Numbers cannot start with '+'")
    
    if num_str.endswith('.'):
        raise ValueError("Numbers cannot end with decimal point")
    
    # Parse as float if it has exponent or decimal point
    if 'e' in num_str.lower() or '.' in num_str:
        try:
            return float(num_str), idx
        except ValueError:
            raise ValueError(f"Invalid number format: {num_str}")
    else:
        # Integer
        try:
            return int(num_str), idx
        except ValueError:
            raise ValueError(f"Invalid number format: {num_str}")