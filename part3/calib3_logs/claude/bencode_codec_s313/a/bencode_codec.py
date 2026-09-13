def bencode(obj: object) -> bytes:
    """Encode an object to bencode format."""
    if isinstance(obj, int):
        # Check for bool (which is a subclass of int in Python)
        if isinstance(obj, bool):
            raise ValueError("bool type not supported")
        return f'i{obj}e'.encode('ascii')
    elif isinstance(obj, bytes):
        return f'{len(obj)}:'.encode('ascii') + obj
    elif isinstance(obj, str):
        encoded_str = obj.encode('utf-8')
        return f'{len(encoded_str)}:'.encode('ascii') + encoded_str
    elif isinstance(obj, list):
        result = b'l'
        for item in obj:
            result += bencode(item)
        result += b'e'
        return result
    elif isinstance(obj, dict):
        # Check that all keys are strings
        for key in obj.keys():
            if not isinstance(key, str):
                raise ValueError("dict keys must be strings")
        
        # Sort keys by their encoded bytes representation
        sorted_keys = sorted(obj.keys(), key=lambda k: k.encode('utf-8'))
        
        result = b'd'
        for key in sorted_keys:
            # Encode the key as a string (UTF-8 bytes with length prefix)
            encoded_key = key.encode('utf-8')
            result += f'{len(encoded_key)}:'.encode('ascii') + encoded_key
            # Encode the value
            result += bencode(obj[key])
        result += b'e'
        return result
    elif isinstance(obj, float):
        raise ValueError("float type not supported")
    elif obj is None:
        raise ValueError("None type not supported")
    else:
        raise ValueError(f"unsupported type: {type(obj)}")


def bdecode(data: bytes) -> object:
    """Decode bencode format to an object."""
    if not data:
        raise ValueError("empty input")
    
    result, pos = _bdecode_value(data, 0)
    
    # Check for trailing data
    if pos != len(data):
        raise ValueError("trailing data after value")
    
    return result


def _bdecode_value(data: bytes, pos: int) -> tuple:
    """Decode a single bencode value starting at position pos.
    Returns (value, new_position)."""
    if pos >= len(data):
        raise ValueError("unexpected end of data")
    
    first_byte = data[pos:pos+1]
    
    if first_byte == b'i':
        # Integer: i<decimal>e
        return _bdecode_int(data, pos)
    elif first_byte == b'l':
        # List: l...e
        return _bdecode_list(data, pos)
    elif first_byte == b'd':
        # Dict: d...e
        return _bdecode_dict(data, pos)
    elif first_byte.isdigit():
        # Byte string: <length>:<data>
        return _bdecode_bytes(data, pos)
    else:
        raise ValueError(f"unexpected byte: {first_byte}")


def _bdecode_int(data: bytes, pos: int) -> tuple:
    """Decode an integer starting at position pos."""
    pos += 1  # skip 'i'
    
    if pos >= len(data):
        raise ValueError("unterminated integer")
    
    end_pos = data.find(b'e', pos)
    if end_pos == -1:
        raise ValueError("unterminated integer")
    
    int_str = data[pos:end_pos].decode('ascii')
    
    # Validate integer format
    if not int_str:
        raise ValueError("empty integer")
    
    # Check for leading zeros (but '0' alone is valid)
    if len(int_str) > 1 and int_str[0] == '0':
        raise ValueError("integer with leading zeros")
    
    # Check for '-0'
    if int_str == '-0':
        raise ValueError("integer -0 not allowed")
    
    # Check for bare '-'
    if int_str == '-':
        raise ValueError("bare minus sign")
    
    try:
        value = int(int_str)
    except ValueError:
        raise ValueError("invalid integer format")
    
    return value, end_pos + 1


def _bdecode_bytes(data: bytes, pos: int) -> tuple:
    """Decode a byte string starting at position pos."""
    # Parse the length prefix
    colon_pos = data.find(b':', pos)
    if colon_pos == -1:
        raise ValueError("no colon in length prefix")
    
    length_str = data[pos:colon_pos].decode('ascii')
    
    # Validate length format
    if not length_str:
        raise ValueError("empty length prefix")
    
    # Check for leading zeros
    if len(length_str) > 1 and length_str[0] == '0':
        raise ValueError("length prefix with leading zeros")
    
    try:
        length = int(length_str)
    except ValueError:
        raise ValueError("invalid length prefix")
    
    if length < 0:
        raise ValueError("negative length")
    
    # Check if we have enough data
    data_start = colon_pos + 1
    data_end = data_start + length
    
    if data_end > len(data):
        raise ValueError("length prefix longer than remaining data")
    
    return data[data_start:data_end], data_end


def _bdecode_list(data: bytes, pos: int) -> tuple:
    """Decode a list starting at position pos."""
    pos += 1  # skip 'l'
    result = []
    
    while pos < len(data):
        if data[pos:pos+1] == b'e':
            return result, pos + 1
        
        value, pos = _bdecode_value(data, pos)
        result.append(value)
    
    raise ValueError("unterminated list")


def _bdecode_dict(data: bytes, pos: int) -> tuple:
    """Decode a dictionary starting at position pos."""
    pos += 1  # skip 'd'
    result = {}
    last_key = None
    
    while pos < len(data):
        if data[pos:pos+1] == b'e':
            return result, pos + 1
        
        # Keys must be byte strings
        if not data[pos:pos+1].isdigit():
            raise ValueError("dict key must be a byte string")
        
        key, pos = _bdecode_bytes(data, pos)
        
        # Check that keys are in sorted order
        if last_key is not None and key < last_key:
            raise ValueError("dict keys not in sorted order")
        last_key = key
        
        # Decode the value
        if pos >= len(data):
            raise ValueError("unterminated dict")
        
        value, pos = _bdecode_value(data, pos)
        result[key] = value
    
    raise ValueError("unterminated dict")
