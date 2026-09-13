
def bencode(obj):
    if isinstance(obj, int):
        return f"i{obj}e".encode('ascii')
    elif isinstance(obj, bytes):
        return f"{len(obj)}:".encode('ascii') + obj
    elif isinstance(obj, str):
        return bencode(obj.encode('utf-8'))
    elif isinstance(obj, list):
        return b'l' + b''.join(bencode(item) for item in obj) + b'e'
    elif isinstance(obj, dict):
        if not all(isinstance(k, str) for k in obj.keys()):
            raise ValueError("Dictionary keys must be strings")
        
        encoded_items = []
        for k, v in obj.items():
            encoded_key = bencode(k)
            encoded_value = bencode(v)
            encoded_items.append((encoded_key, encoded_value))

        encoded_items.sort(key=lambda x: x[0])

        result = b'd'
        for k_encoded, v_encoded in encoded_items:
            result += k_encoded
            result += v_encoded
        result += b'e'
        return result
    else:
        raise ValueError(f"Unsupported type: {type(obj)}")

def bdecode(data):
    if not isinstance(data, bytes):
        raise TypeError("Input must be bytes")
    if not data:
        raise ValueError("Empty input")
        
    obj, length = _bdecode_recursive(data, 0)
    
    if length != len(data):
        raise ValueError("Trailing data")
        
    return obj

def _bdecode_recursive(data, index):
    if index >= len(data):
        raise ValueError("Unexpected end of data")

    marker = data[index:index+1]

    if marker == b'i':
        end_index = data.find(b'e', index + 1)
        if end_index == -1:
            raise ValueError("Unterminated integer")
        
        num_str = data[index + 1:end_index].decode('ascii')
        
        if not num_str or num_str == '-':
             raise ValueError("Invalid integer")

        if (num_str.startswith('0') and len(num_str) > 1) or num_str == '-0':
            raise ValueError("Integer with leading zero")
            
        try:
            val = int(num_str)
            return val, end_index + 1
        except ValueError:
            raise ValueError("Invalid integer format")

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
        items = {}
        last_key = None
        while index < len(data) and data[index:index+1] != b'e':
            key, new_index = _bdecode_recursive(data, index)
            if not isinstance(key, bytes):
                raise ValueError("Dictionary key must be bytes")

            # As per standard, keys must be sorted, but we don't enforce on decode
            # just that they are valid bencoded strings.
            
            value, new_index_val = _bdecode_recursive(data, new_index)
            items[key] = value
            index = new_index_val

        if index >= len(data) or data[index:index+1] != b'e':
            raise ValueError("Unterminated dictionary")
            
        return items, index + 1

    elif marker.isdigit():
        colon_index = data.find(b':', index)
        if colon_index == -1:
            raise ValueError("Invalid string length prefix")
            
        len_str = data[index:colon_index].decode('ascii')

        if len_str.startswith('0') and len(len_str) > 1:
            raise ValueError("String length with leading zero")

        try:
            length = int(len_str)
        except ValueError:
            raise ValueError("Invalid string length")

        start = colon_index + 1
        end = start + length
        
        if end > len(data):
            raise ValueError("String length exceeds data")
            
        return data[start:end], end
    
    else:
        raise ValueError(f"Unexpected byte at index {index}")
