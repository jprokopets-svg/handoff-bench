def bencode(obj: object) -> bytes:
    """Encode a Python object to bencode format (bytes)."""
    if isinstance(obj, bool):
        raise ValueError("bool type not supported")
    if isinstance(obj, int):
        return b'i' + str(obj).encode() + b'e'
    if isinstance(obj, bytes):
        return str(len(obj)).encode() + b':' + obj
    if isinstance(obj, str):
        encoded_str = obj.encode('utf-8')
        return str(len(encoded_str)).encode() + b':' + encoded_str
    if isinstance(obj, list):
        result = b'l'
        for item in obj:
            result += bencode(item)
        result += b'e'
        return result
    if isinstance(obj, dict):
        result = b'd'
        # Sort keys lexicographically by their encoded bytes
        sorted_items = sorted(obj.items(), key=lambda kv: _encode_key(kv[0]))
        for key, value in sorted_items:
            if not isinstance(key, str):
                raise ValueError("dict keys must be strings")
            result += bencode(key)
            result += bencode(value)
        result += b'e'
        return result
    raise ValueError(f"unsupported type: {type(obj)}")


def _encode_key(key: str) -> bytes:
    """Encode a dict key to bytes for sorting purposes."""
    return key.encode('utf-8')


def bdecode(data: bytes) -> object:
    """Decode bencode format (bytes) to a Python object."""
    if not data:
        raise ValueError("empty input")
    
    result, pos = _bdecode_value(data, 0)
    
    if pos != len(data):
        raise ValueError("trailing data after value")
    
    return result


def _bdecode_value(data: bytes, pos: int) -> tuple:
    """Decode a single bencode value starting at position pos.
    Returns (value, new_position)."""
    if pos >= len(data):
        raise ValueError("unexpected end of data")
    
    ch = data[pos:pos+1]
    
    if ch == b'i':
        return _bdecode_int(data, pos)
    elif ch == b'l':
        return _bdecode_list(data, pos)
    elif ch == b'd':
        return _bdecode_dict(data, pos)
    elif ch.isdigit():
        return _bdecode_bytes(data, pos)
    else:
        raise ValueError(f"unexpected byte: {ch}")


def _bdecode_int(data: bytes, pos: int) -> tuple:
    """Decode an integer starting at position pos (after 'i').
    Returns (value, new_position)."""
    pos += 1  # skip 'i'
    
    end = data.find(b'e', pos)
    if end == -1:
        raise ValueError("unterminated integer")
    
    int_str = data[pos:end].decode('ascii', errors='strict')
    
    # Validate integer format
    if not int_str:
        raise ValueError("empty integer")
    
    # Check for leading zeros (but '0' alone is valid)
    if int_str[0] == '0' and len(int_str) > 1:
        raise ValueError("integer with leading zeros")
    
    # Check for bare '-'
    if int_str == '-':
        raise ValueError("bare minus sign")
    
    # Check for -0
    if int_str == '-0':
        raise ValueError("negative zero")
    
    value = int(int_str)
    return value, end + 1


def _bdecode_bytes(data: bytes, pos: int) -> tuple:
    """Decode a byte string starting at position pos.
    Returns (value, new_position)."""
    # Parse length prefix
    colon = data.find(b':', pos)
    if colon == -1:
        raise ValueError("no colon in length prefix")
    
    length_str = data[pos:colon].decode('ascii', errors='strict')
    
    # Validate length format
    if not length_str:
        raise ValueError("empty length prefix")
    
    # Check for leading zeros
    if length_str[0] == '0' and len(length_str) > 1:
        raise ValueError("length prefix with leading zeros")
    
    length = int(length_str)
    
    # Check if we have enough data
    start = colon + 1
    end = start + length
    if end > len(data):
        raise ValueError("length prefix longer than remaining data")
    
    return data[start:end], end


def _bdecode_list(data: bytes, pos: int) -> tuple:
    """Decode a list starting at position pos (after 'l').
    Returns (value, new_position)."""
    pos += 1  # skip 'l'
    result = []
    
    while pos < len(data):
        if data[pos:pos+1] == b'e':
            return result, pos + 1
        
        value, pos = _bdecode_value(data, pos)
        result.append(value)
    
    raise ValueError("unterminated list")


def _bdecode_dict(data: bytes, pos: int) -> tuple:
    """Decode a dictionary starting at position pos (after 'd').
    Returns (value, new_position)."""
    pos += 1  # skip 'd'
    result = {}
    
    while pos < len(data):
        if data[pos:pos+1] == b'e':
            return result, pos + 1
        
        # Keys must be byte strings
        if not data[pos:pos+1].isdigit():
            raise ValueError("non-bytes dict key")
        
        key, pos = _bdecode_bytes(data, pos)
        
        if pos >= len(data):
            raise ValueError("unterminated dict")
        
        value, pos = _bdecode_value(data, pos)
        result[key] = value
    
    raise ValueError("unterminated dict")
