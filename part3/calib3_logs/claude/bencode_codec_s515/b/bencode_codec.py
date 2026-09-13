def bencode(obj: object) -> bytes:
    """Encode a Python object to bencode format (bytes)."""
    if isinstance(obj, bool) or isinstance(obj, type(None)):
        raise ValueError(f"Cannot bencode {type(obj).__name__}")
    
    if isinstance(obj, int):
        return f'i{obj}e'.encode('ascii')
    
    if isinstance(obj, bytes):
        return f'{len(obj)}:'.encode('ascii') + obj
    
    if isinstance(obj, str):
        encoded = obj.encode('utf-8')
        return f'{len(encoded)}:'.encode('ascii') + encoded
    
    if isinstance(obj, list):
        result = b'l'
        for item in obj:
            result += bencode(item)
        result += b'e'
        return result
    
    if isinstance(obj, dict):
        result = b'd'
        # Sort keys lexicographically by their encoded bytes
        items = []
        for key, value in obj.items():
            if not isinstance(key, str):
                raise ValueError(f"Dict keys must be str, got {type(key).__name__}")
            encoded_key = key.encode('utf-8')
            items.append((encoded_key, bencode(value)))
        
        # Sort by encoded key bytes
        items.sort(key=lambda x: x[0])
        
        for encoded_key, encoded_value in items:
            result += f'{len(encoded_key)}:'.encode('ascii') + encoded_key + encoded_value
        result += b'e'
        return result
    
    raise ValueError(f"Cannot bencode {type(obj).__name__}")


def bdecode(data: bytes) -> object:
    """Decode bencode format (bytes) to a Python object."""
    if not data:
        raise ValueError("Empty input")
    
    obj, pos = _decode_value(data, 0)
    
    # Check for trailing data
    if pos != len(data):
        raise ValueError("Trailing data after value")
    
    return obj


def _decode_value(data: bytes, pos: int) -> tuple:
    """Decode a single value starting at position pos. Returns (value, new_pos)."""
    if pos >= len(data):
        raise ValueError("Unexpected end of input")
    
    ch = data[pos:pos+1]
    
    if ch == b'i':
        return _decode_int(data, pos)
    elif ch == b'l':
        return _decode_list(data, pos)
    elif ch == b'd':
        return _decode_dict(data, pos)
    elif ch.isdigit():
        return _decode_bytes(data, pos)
    else:
        raise ValueError(f"Unexpected byte: {ch}")


def _decode_int(data: bytes, pos: int) -> tuple:
    """Decode an integer (i<num>e format). Returns (int_value, new_pos)."""
    pos += 1  # skip 'i'
    
    if pos >= len(data):
        raise ValueError("Unterminated integer")
    
    start = pos
    
    # Handle negative sign
    if data[pos:pos+1] == b'-':
        pos += 1
        if pos >= len(data):
            raise ValueError("Unterminated integer")
    
    # Must have at least one digit
    if pos >= len(data) or not data[pos:pos+1].isdigit():
        raise ValueError("Invalid integer format")
    
    # Collect digits
    while pos < len(data) and data[pos:pos+1].isdigit():
        pos += 1
    
    if pos >= len(data) or data[pos:pos+1] != b'e':
        raise ValueError("Unterminated integer")
    
    num_str = data[start:pos].decode('ascii')
    
    # Check for leading zeros (except "0" itself)
    if num_str.startswith('0') and len(num_str) > 1:
        raise ValueError("Leading zeros in integer")
    
    # Check for "-0"
    if num_str == '-0':
        raise ValueError("Invalid integer: -0")
    
    # Check for bare "-"
    if num_str == '-':
        raise ValueError("Invalid integer: bare minus")
    
    return int(num_str), pos + 1


def _decode_bytes(data: bytes, pos: int) -> tuple:
    """Decode a byte string (<len>:<data> format). Returns (bytes_value, new_pos)."""
    start = pos
    
    # Check for leading zeros in length
    if data[pos:pos+1] == b'0':
        # "0:" is valid, but "0X:" where X is a digit is not
        if pos + 1 < len(data) and data[pos+1:pos+2].isdigit():
            raise ValueError("Leading zeros in length prefix")
    
    # Collect digits
    while pos < len(data) and data[pos:pos+1].isdigit():
        pos += 1
    
    if pos >= len(data) or data[pos:pos+1] != b':':
        raise ValueError("Invalid byte string format")
    
    length_str = data[start:pos].decode('ascii')
    length = int(length_str)
    
    pos += 1  # skip ':'
    
    # Check if we have enough data
    if pos + length > len(data):
        raise ValueError("Insufficient data for byte string")
    
    result = data[pos:pos+length]
    return result, pos + length


def _decode_list(data: bytes, pos: int) -> tuple:
    """Decode a list (l<items>e format). Returns (list_value, new_pos)."""
    pos += 1  # skip 'l'
    result = []
    
    while pos < len(data):
        if data[pos:pos+1] == b'e':
            return result, pos + 1
        
        item, pos = _decode_value(data, pos)
        result.append(item)
    
    raise ValueError("Unterminated list")


def _decode_dict(data: bytes, pos: int) -> tuple:
    """Decode a dictionary (d<key><value>...e format). Returns (dict_value, new_pos)."""
    pos += 1  # skip 'd'
    result = {}
    last_key = None
    
    while pos < len(data):
        if data[pos:pos+1] == b'e':
            return result, pos + 1
        
        # Keys must be byte strings
        if not data[pos:pos+1].isdigit():
            raise ValueError("Dict key must be a byte string")
        
        key, pos = _decode_bytes(data, pos)
        
        # Check lexicographic ordering
        if last_key is not None and key < last_key:
            raise ValueError("Dict keys not in lexicographic order")
        last_key = key
        
        if pos >= len(data):
            raise ValueError("Unterminated dict")
        
        value, pos = _decode_value(data, pos)
        result[key] = value
    
    raise ValueError("Unterminated dict")
