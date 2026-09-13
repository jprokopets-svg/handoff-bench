def bencode(obj: object) -> bytes:
    """Encode an object to bencode format."""
    if isinstance(obj, int):
        # Check for bool (bool is subclass of int in Python)
        if isinstance(obj, bool):
            raise ValueError("bool type not supported")
        return f'i{obj}e'.encode('ascii')
    elif isinstance(obj, bytes):
        return f'{len(obj)}:'.encode('ascii') + obj
    elif isinstance(obj, str):
        encoded_bytes = obj.encode('utf-8')
        return f'{len(encoded_bytes)}:'.encode('ascii') + encoded_bytes
    elif isinstance(obj, list):
        result = b'l'
        for item in obj:
            result += bencode(item)
        result += b'e'
        return result
    elif isinstance(obj, dict):
        # Keys must be strings
        for key in obj.keys():
            if not isinstance(key, str):
                raise ValueError("dict keys must be strings")
        
        # Sort keys by their encoded bytes representation
        sorted_keys = sorted(obj.keys(), key=lambda k: k.encode('utf-8'))
        
        result = b'd'
        for key in sorted_keys:
            # Encode key as string (UTF-8 bytes with length prefix)
            key_encoded = key.encode('utf-8')
            result += f'{len(key_encoded)}:'.encode('ascii') + key_encoded
            # Encode value
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
    """Decode a single value starting at position pos.
    Returns (value, new_position)
    """
    if pos >= len(data):
        raise ValueError("unexpected end of data")
    
    first_byte = data[pos:pos+1]
    
    if first_byte == b'i':
        # Integer
        return _bdecode_int(data, pos)
    elif first_byte == b'l':
        # List
        return _bdecode_list(data, pos)
    elif first_byte == b'd':
        # Dictionary
        return _bdecode_dict(data, pos)
    elif first_byte.isdigit():
        # Byte string
        return _bdecode_string(data, pos)
    else:
        raise ValueError(f"unexpected byte: {first_byte}")


def _bdecode_int(data: bytes, pos: int) -> tuple:
    """Decode an integer starting at position pos.
    Format: i<decimal>e
    """
    pos += 1  # skip 'i'
    
    if pos >= len(data):
        raise ValueError("unterminated integer")
    
    # Find the 'e'
    end_pos = data.find(b'e', pos)
    if end_pos == -1:
        raise ValueError("unterminated integer")
    
    int_str = data[pos:end_pos].decode('ascii')
    
    if not int_str:
        raise ValueError("empty integer")
    
    # Check for leading zeros (but '0' alone is valid)
    if int_str[0] == '0' and len(int_str) > 1:
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
        raise ValueError(f"invalid integer: {int_str}")
    
    return value, end_pos + 1


def _bdecode_string(data: bytes, pos: int) -> tuple:
    """Decode a byte string starting at position pos.
    Format: <length>:<bytes>
    """
    # Find the ':'
    colon_pos = data.find(b':', pos)
    if colon_pos == -1:
        raise ValueError("unterminated string length")
    
    length_str = data[pos:colon_pos].decode('ascii')
    
    if not length_str:
        raise ValueError("empty length")
    
    # Check for leading zeros
    if length_str[0] == '0' and len(length_str) > 1:
        raise ValueError("length prefix with leading zeros")
    
    try:
        length = int(length_str)
    except ValueError:
        raise ValueError(f"invalid length: {length_str}")
    
    if length < 0:
        raise ValueError("negative length")
    
    string_start = colon_pos + 1
    string_end = string_start + length
    
    if string_end > len(data):
        raise ValueError("length prefix longer than remaining data")
    
    return data[string_start:string_end], string_end


def _bdecode_list(data: bytes, pos: int) -> tuple:
    """Decode a list starting at position pos.
    Format: l<items>e
    """
    pos += 1  # skip 'l'
    result = []
    
    while pos < len(data):
        if data[pos:pos+1] == b'e':
            return result, pos + 1
        
        value, pos = _bdecode_value(data, pos)
        result.append(value)
    
    raise ValueError("unterminated list")


def _bdecode_dict(data: bytes, pos: int) -> tuple:
    """Decode a dictionary starting at position pos.
    Format: d<key><value>...<key><value>e
    Keys must be byte strings and must be sorted lexicographically.
    """
    pos += 1  # skip 'd'
    result = {}
    last_key = None
    
    while pos < len(data):
        if data[pos:pos+1] == b'e':
            return result, pos + 1
        
        # Keys must be strings (byte strings)
        if not data[pos:pos+1].isdigit():
            raise ValueError("dict key must be a string")
        
        key, pos = _bdecode_string(data, pos)
        
        # Check that keys are sorted
        if last_key is not None and key < last_key:
            raise ValueError("dict keys not sorted")
        last_key = key
        
        if pos >= len(data):
            raise ValueError("unterminated dict")
        
        value, pos = _bdecode_value(data, pos)
        result[key] = value
    
    raise ValueError("unterminated dict")
