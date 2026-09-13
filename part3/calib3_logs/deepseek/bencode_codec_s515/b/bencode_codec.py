def bencode(obj: object) -> bytes:
    """Encode Python object to bencoded bytes."""
    if isinstance(obj, int):
        if obj == 0:
            return b'i0e'
        return f'i{obj}e'.encode()
    elif isinstance(obj, bytes):
        return f'{len(obj)}:'.encode() + obj
    elif isinstance(obj, str):
        # Convert string to UTF-8 bytes
        utf8_bytes = obj.encode('utf-8')
        return f'{len(utf8_bytes)}:'.encode() + utf8_bytes
    elif isinstance(obj, list):
        encoded_items = b''.join(bencode(item) for item in obj)
        return b'l' + encoded_items + b'e'
    elif isinstance(obj, dict):
        # Keys must be strings
        for key in obj.keys():
            if not isinstance(key, str):
                raise ValueError(f"Dictionary key must be str, got {type(key)}")
        
        # Sort keys lexicographically by their raw encoded bytes
        sorted_items = sorted(obj.items(), key=lambda kv: kv[0].encode('utf-8'))
        encoded_items = b''
        for key, value in sorted_items:
            encoded_items += bencode(key) + bencode(value)
        return b'd' + encoded_items + b'e'
    else:
        raise ValueError(f"Cannot bencode type {type(obj)}")


def bdecode(data: bytes) -> object:
    """Decode bencoded bytes to Python object."""
    if not data:
        raise ValueError("Empty input")
    
    idx = 0
    length = len(data)
    
    def parse() -> object:
        nonlocal idx
        if idx >= length:
            raise ValueError("Unexpected end of data")
        
        c = data[idx:idx+1]
        
        # Parse integer
        if c == b'i':
            idx += 1
            start = idx
            # Find the ending 'e'
            while idx < length and data[idx:idx+1] != b'e':
                idx += 1
            
            if idx >= length:
                raise ValueError("Unterminated integer")
            
            # Extract integer string
            int_str = data[start:idx].decode('ascii')
            idx += 1  # Skip 'e'
            
            # Validate integer format
            if not int_str:
                raise ValueError("Empty integer")
            if int_str == '-':
                raise ValueError("Invalid integer: '-'")
            if int_str[0] == '0' and len(int_str) > 1:
                raise ValueError("Integer with leading zeros")
            if int_str == '-0':
                raise ValueError("Invalid integer: '-0'")
            
            return int(int_str)
        
        # Parse string (bytes)
        elif c in b'0123456789':
            # Parse length
            start = idx
            while idx < length and data[idx:idx+1] in b'0123456789':
                idx += 1
            
            if idx >= length or data[idx:idx+1] != b':':
                raise ValueError("Missing ':' in string length")
            
            length_str = data[start:idx].decode('ascii')
            idx += 1  # Skip ':'
            
            # Validate length format
            if length_str == '':
                raise ValueError("Empty length prefix")
            if length_str[0] == '0' and len(length_str) > 1:
                raise ValueError("Length with leading zeros")
            
            str_len = int(length_str)
            
            # Check if we have enough data
            if idx + str_len > length:
                raise ValueError("String length exceeds available data")
            
            # Extract bytes
            result = data[idx:idx+str_len]
            idx += str_len
            return result
        
        # Parse list
        elif c == b'l':
            idx += 1
            result = []
            while idx < length and data[idx:idx+1] != b'e':
                result.append(parse())
            
            if idx >= length:
                raise ValueError("Unterminated list")
            
            idx += 1  # Skip 'e'
            return result
        
        # Parse dictionary
        elif c == b'd':
            idx += 1
            result = {}
            while idx < length and data[idx:idx+1] != b'e':
                # Parse key
                key = parse()
                if not isinstance(key, bytes):
                    raise ValueError("Dictionary key must be bytes")
                
                # Parse value
                value = parse()
                result[key] = value
            
            if idx >= length:
                raise ValueError("Unterminated dictionary")
            
            idx += 1  # Skip 'e'
            return result
        
        else:
            raise ValueError(f"Unexpected byte: {c}")
    
    result = parse()
    
    # Check for trailing data
    if idx < length:
        raise ValueError("Trailing data after parsed value")
    
    return result