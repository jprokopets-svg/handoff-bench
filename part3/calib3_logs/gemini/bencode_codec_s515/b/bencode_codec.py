
def bencode(obj: object) -> bytes:
    if isinstance(obj, int):
        return f'i{obj}e'.encode('ascii')
    elif isinstance(obj, bytes):
        return f'{len(obj)}:'.encode('ascii') + obj
    elif isinstance(obj, str):
        return bencode(obj.encode('utf-8'))
    elif isinstance(obj, list):
        return b'l' + b''.join(bencode(item) for item in obj) + b'e'
    elif isinstance(obj, dict):
        if not all(isinstance(k, str) for k in obj.keys()):
            raise ValueError("Dictionary keys must be strings")
        
        sorted_items = sorted(obj.items())
        
        encoded_items = []
        for k, v in sorted_items:
            encoded_items.append(bencode(k) + bencode(v))

        return b'd' + b''.join(encoded_items) + b'e'
    else:
        raise ValueError(f"Unsupported type: {type(obj)}")


def bdecode(data: bytes) -> object:
    if not isinstance(data, bytes):
        raise TypeError("bdecode input must be bytes")
    if not data:
        raise ValueError("Empty input")

    obj, length = _bdecode_recursive(data, 0)
    if length != len(data):
        raise ValueError("Trailing data")
    return obj

def _bdecode_recursive(data: bytes, index: int):
    if index >= len(data):
        raise ValueError("Unexpected end of data")

    marker = data[index:index+1]

    if marker == b'i':
        end_index = data.find(b'e', index + 1)
        if end_index == -1:
            raise ValueError("Unterminated integer")
        
        num_str = data[index + 1:end_index].decode('ascii')
        if not num_str or num_str == '-':
             raise ValueError("Invalid integer representation")
        if (num_str.startswith('0') and len(num_str) > 1) or num_str == '-0':
            raise ValueError("Integer with leading zeros or -0")
            
        try:
            val = int(num_str)
        except ValueError:
            raise ValueError("Invalid integer")

        return val, end_index + 1

    elif marker in b'0123456789':
        colon_index = data.find(b':', index)
        if colon_index == -1:
            raise ValueError("Unterminated string")
        
        len_str = data[index:colon_index].decode('ascii')
        if len_str.startswith('0') and len(len_str) > 1:
            raise ValueError("Length prefix with leading zeros")

        try:
            length = int(len_str)
        except ValueError:
            raise ValueError("Invalid length prefix")

        start = colon_index + 1
        end = start + length
        if end > len(data):
            raise ValueError("String length exceeds data bounds")
        
        return data[start:end], end

    elif marker == b'l':
        index += 1
        items = []
        while index < len(data) and data[index:index+1] != b'e':
            item, index = _bdecode_recursive(data, index)
            items.append(item)
        
        if index >= len(data) or data[index:index+1] != b'e':
            raise ValueError("Unterminated list")
            
        return items, index + 1

    elif marker == b'd':
        index += 1
        d = {}
        last_key = None
        while index < len(data) and data[index:index+1] != b'e':
            key, index = _bdecode_recursive(data, index)
            if not isinstance(key, bytes):
                raise ValueError("Dictionary keys must be bytes")
            
            # As per spec, keys must be sorted. 
            # This check is not always enforced by decoders, but it's good practice.
            if last_key is not None and last_key >= key:
                raise ValueError("Dictionary keys not sorted")
            last_key = key

            value, index = _bdecode_recursive(data, index)
            d[key] = value
        
        if index >= len(data) or data[index:index+1] != b'e':
            raise ValueError("Unterminated dictionary")

        return d, index + 1

    else:
        raise ValueError("Invalid bencode data")
