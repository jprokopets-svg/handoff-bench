def bencode(obj: object) -> bytes:
    """Encode Python object to bencode bytes."""
    if isinstance(obj, bool):
        raise ValueError(f"Unsupported type: {type(obj)}")
    if isinstance(obj, int):
        return f"i{obj}e".encode()
    elif isinstance(obj, bytes):
        return f"{len(obj)}:".encode() + obj
    elif isinstance(obj, str):
        # Convert string to UTF-8 bytes
        utf8_bytes = obj.encode('utf-8')
        return f"{len(utf8_bytes)}:".encode() + utf8_bytes
    elif isinstance(obj, list):
        encoded_items = b''.join(bencode(item) for item in obj)
        return b'l' + encoded_items + b'e'
    elif isinstance(obj, dict):
        # Keys must be strings, sorted lexicographically by their raw encoded bytes
        # Convert keys to UTF-8 bytes for sorting
        sorted_items = []
        for key, value in obj.items():
            if not isinstance(key, str):
                raise ValueError("Dictionary keys must be strings")
            key_bytes = key.encode('utf-8')
            sorted_items.append((key_bytes, value))
        
        # Sort by raw bytes
        sorted_items.sort(key=lambda x: x[0])
        
        encoded_items = b''
        for key_bytes, value in sorted_items:
            encoded_items += bencode(key_bytes) + bencode(value)
        
        return b'd' + encoded_items + b'e'
    else:
        raise ValueError(f"Unsupported type: {type(obj)}")


def bdecode(data: bytes) -> object:
    """Decode bencode bytes to Python object."""
    if not data:
        raise ValueError("Empty input")
    
    idx = 0
    result, idx = _bdecode(data, idx)
    
    # Check for trailing data
    if idx != len(data):
        raise ValueError("Trailing data after value")
    
    return result


def _bdecode(data: bytes, idx: int):
    """Helper function to decode from position idx."""
    if idx >= len(data):
        raise ValueError("Unexpected end of data")
    
    c = data[idx]
    
    # Integer
    if c == ord('i'):
        idx += 1
        start = idx
        
        # Find 'e'
        while idx < len(data) and data[idx] != ord('e'):
            idx += 1
        
        if idx >= len(data):
            raise ValueError("Unterminated integer")
        
        int_str = data[start:idx].decode()
        idx += 1  # Skip 'e'
        
        # Validate integer format
        if not int_str:
            raise ValueError("Empty integer")
        
        if int_str == '-':
            raise ValueError("Bare '-'")
        
        if int_str == '0' and start != idx - 2:  # i0e is fine, but i01e is not
            # Actually need to check for leading zeros
            if data[start] == ord('0') and (idx - start - 1) > 1:
                raise ValueError("Integer with leading zeros")
        
        if int_str.startswith('-0'):
            raise ValueError("Negative zero")
        
        # Check for leading zeros in positive numbers
        if int_str[0] != '-' and len(int_str) > 1 and int_str[0] == '0':
            raise ValueError("Integer with leading zeros")
        
        return int(int_str), idx
    
    # List
    elif c == ord('l'):
        idx += 1
        result = []
        
        while idx < len(data) and data[idx] != ord('e'):
            item, idx = _bdecode(data, idx)
            result.append(item)
        
        if idx >= len(data):
            raise ValueError("Unterminated list")
        
        idx += 1  # Skip 'e'
        return result, idx
    
    # Dictionary
    elif c == ord('d'):
        idx += 1
        result = {}
        
        while idx < len(data) and data[idx] != ord('e'):
            # Decode key (must be bytes)
            key, idx = _bdecode(data, idx)
            
            if not isinstance(key, bytes):
                raise ValueError("Dictionary key must be bytes")
            
            # Decode value
            value, idx = _bdecode(data, idx)
            
            result[key] = value
        
        if idx >= len(data):
            raise ValueError("Unterminated dictionary")
        
        idx += 1  # Skip 'e'
        return result, idx
    
    # String/bytes (length-prefixed)
    elif ord('0') <= c <= ord('9'):
        # Parse length
        start = idx
        while idx < len(data) and ord('0') <= data[idx] <= ord('9'):
            idx += 1
        
        if idx >= len(data) or data[idx] != ord(':'):
            raise ValueError("Missing ':' in string length")
        
        length_str = data[start:idx].decode()
        
        # Check for leading zeros
        if len(length_str) > 1 and length_str[0] == '0':
            raise ValueError("String length with leading zeros")
        
        length = int(length_str)
        idx += 1  # Skip ':'
        
        # Check if we have enough data
        if idx + length > len(data):
            raise ValueError("String length exceeds available data")
        
        result = data[idx:idx + length]
        idx += length
        return result, idx
    
    else:
        raise ValueError(f"Unexpected byte: {chr(c)}")