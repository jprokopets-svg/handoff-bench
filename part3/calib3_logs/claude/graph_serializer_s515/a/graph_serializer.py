"""
Graph serializer that preserves shared references and cycles.
"""

def encode(obj):
    """
    Encode a Python object to a string, preserving shared references and cycles.
    
    Supported types: int, float, bool, None, str, list, dict (with string keys)
    
    Args:
        obj: The object to encode
        
    Returns:
        A string representation of the object
        
    Raises:
        ValueError: If the object contains unsupported types
    """
    seen = {}  # Maps id(obj) -> reference_id
    ref_counter = [0]  # Mutable counter for reference IDs
    
    def get_ref_id(obj_id):
        if obj_id not in seen:
            seen[obj_id] = ref_counter[0]
            ref_counter[0] += 1
        return seen[obj_id]
    
    def encode_value(val):
        # Handle primitive types that don't need reference tracking
        if val is None:
            return "N"
        elif isinstance(val, bool):
            return "B" + ("T" if val else "F")
        elif isinstance(val, int):
            return "I" + str(val)
        elif isinstance(val, float):
            return "F" + str(val)
        elif isinstance(val, str):
            # Encode string with length prefix to handle special chars
            encoded_str = val.encode('utf-8')
            return "S" + str(len(encoded_str)) + ":" + val
        elif isinstance(val, list):
            ref_id = get_ref_id(id(val))
            # Mark as a reference to handle cycles
            result = "L" + str(ref_id) + "["
            for item in val:
                result += encode_value(item)
            result += "]"
            return result
        elif isinstance(val, dict):
            ref_id = get_ref_id(id(val))
            result = "D" + str(ref_id) + "{"
            for key, value in val.items():
                if not isinstance(key, str):
                    raise ValueError(f"Dict keys must be strings, got {type(key)}")
                result += encode_value(key) + ":" + encode_value(value)
            result += "}"
            return result
        else:
            raise ValueError(f"Unsupported type: {type(val)}")
    
    return encode_value(obj)


def decode(s):
    """
    Decode a string back to a Python object, preserving shared references and cycles.
    
    Args:
        s: The encoded string
        
    Returns:
        The decoded object
        
    Raises:
        ValueError: If the input is malformed
    """
    if not isinstance(s, str):
        raise ValueError("Input must be a string")
    
    pos = [0]  # Mutable position tracker
    refs = {}  # Maps reference_id -> object
    
    def decode_value():
        if pos[0] >= len(s):
            raise ValueError("Unexpected end of input")
        
        char = s[pos[0]]
        pos[0] += 1
        
        if char == 'N':
            return None
        elif char == 'B':
            if pos[0] >= len(s):
                raise ValueError("Unexpected end of input")
            val = s[pos[0]]
            pos[0] += 1
            if val == 'T':
                return True
            elif val == 'F':
                return False
            else:
                raise ValueError(f"Invalid boolean value: {val}")
        elif char == 'I':
            # Read integer
            num_str = ""
            while pos[0] < len(s) and s[pos[0]] not in '[]{},":':
                num_str += s[pos[0]]
                pos[0] += 1
            if not num_str:
                raise ValueError("Invalid integer")
            return int(num_str)
        elif char == 'F':
            # Read float
            num_str = ""
            while pos[0] < len(s) and s[pos[0]] not in '[]{},":':
                num_str += s[pos[0]]
                pos[0] += 1
            if not num_str:
                raise ValueError("Invalid float")
            return float(num_str)
        elif char == 'S':
            # Read string with length prefix
            len_str = ""
            while pos[0] < len(s) and s[pos[0]] != ':':
                len_str += s[pos[0]]
                pos[0] += 1
            if pos[0] >= len(s) or s[pos[0]] != ':':
                raise ValueError("Invalid string format")
            pos[0] += 1  # Skip ':'
            
            try:
                byte_len = int(len_str)
            except ValueError:
                raise ValueError("Invalid string length")
            
            # Extract the string
            if pos[0] + len_str > len(s):
                raise ValueError("String length exceeds input")
            
            # We need to extract byte_len bytes from the UTF-8 encoded string
            # But we're working with a string, so we need to be careful
            start_pos = pos[0]
            # Count UTF-8 bytes
            byte_count = 0
            end_pos = start_pos
            while byte_count < byte_len and end_pos < len(s):
                char_bytes = len(s[end_pos].encode('utf-8'))
                byte_count += char_bytes
                end_pos += 1
            
            result = s[start_pos:end_pos]
            pos[0] = end_pos
            return result
        elif char == 'L':
            # Read list with reference ID
            ref_id_str = ""
            while pos[0] < len(s) and s[pos[0]] != '[':
                ref_id_str += s[pos[0]]
                pos[0] += 1
            if pos[0] >= len(s) or s[pos[0]] != '[':
                raise ValueError("Invalid list format")
            pos[0] += 1  # Skip '['
            
            try:
                ref_id = int(ref_id_str)
            except ValueError:
                raise ValueError("Invalid reference ID")
            
            # Create list and store reference before parsing contents (for cycles)
            lst = []
            refs[ref_id] = lst
            
            # Parse list contents
            while pos[0] < len(s) and s[pos[0]] != ']':
                lst.append(decode_value())
            
            if pos[0] >= len(s) or s[pos[0]] != ']':
                raise ValueError("Unexpected end of list")
            pos[0] += 1  # Skip ']'
            
            return lst
        elif char == 'D':
            # Read dict with reference ID
            ref_id_str = ""
            while pos[0] < len(s) and s[pos[0]] != '{':
                ref_id_str += s[pos[0]]
                pos[0] += 1
            if pos[0] >= len(s) or s[pos[0]] != '{':
                raise ValueError("Invalid dict format")
            pos[0] += 1  # Skip '{'
            
            try:
                ref_id = int(ref_id_str)
            except ValueError:
                raise ValueError("Invalid reference ID")
            
            # Create dict and store reference before parsing contents (for cycles)
            dct = {}
            refs[ref_id] = dct
            
            # Parse dict contents
            while pos[0] < len(s) and s[pos[0]] != '}':
                key = decode_value()
                if not isinstance(key, str):
                    raise ValueError("Dict keys must be strings")
                if pos[0] >= len(s) or s[pos[0]] != ':':
                    raise ValueError("Expected ':' after dict key")
                pos[0] += 1  # Skip ':'
                value = decode_value()
                dct[key] = value
            
            if pos[0] >= len(s) or s[pos[0]] != '}':
                raise ValueError("Unexpected end of dict")
            pos[0] += 1  # Skip '}'
            
            return dct
        else:
            raise ValueError(f"Unknown type marker: {char}")
    
    result = decode_value()
    if pos[0] != len(s):
        raise ValueError("Extra data after decoding")
    return result
