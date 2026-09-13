import struct
from typing import Any, Union, Dict, List

def bencode(obj: Any) -> bytes:
    """Encode a Python object to bencode format.
    
    Supported types:
    - int: encoded as i<decimal>e
    - bytes: encoded as <length>:<bytes>
    - str: converted to UTF-8 bytes then encoded as bytes
    - list: encoded as l + concatenated items + e
    - dict: encoded as d + key-value pairs + e, keys must be str,
            sorted lexicographically by their encoded bytes
    
    Raises ValueError for unsupported types.
    """
    # Check for bool first (bool is a subclass of int in Python)
    if isinstance(obj, bool):
        raise ValueError(f"Unsupported type for bencode: {type(obj)}")
    
    if isinstance(obj, int):
        return f"i{obj}e".encode('ascii')
    elif isinstance(obj, bytes):
        return f"{len(obj)}:".encode('ascii') + obj
    elif isinstance(obj, str):
        # Convert to UTF-8 bytes
        data = obj.encode('utf-8')
        return f"{len(data)}:".encode('ascii') + data
    elif isinstance(obj, list):
        encoded_items = b''.join(bencode(item) for item in obj)
        return b'l' + encoded_items + b'e'
    elif isinstance(obj, dict):
        # Check all keys are strings
        for key in obj:
            if not isinstance(key, str):
                raise ValueError(f"Dict key must be str, got {type(key)}")
        
        # Sort keys lexicographically by their encoded bytes
        sorted_items = sorted(obj.items(), key=lambda kv: kv[0].encode('utf-8'))
        
        encoded_pairs = b''
        for key, value in sorted_items:
            encoded_pairs += bencode(key) + bencode(value)
        
        return b'd' + encoded_pairs + b'e'
    else:
        raise ValueError(f"Unsupported type for bencode: {type(obj)}")


def bdecode(data: bytes) -> Any:
    """Decode bencode data to Python object.
    
    Returns:
    - int for i<decimal>e
    - bytes for <length>:<bytes>
    - list for l...e
    - dict for d...e (keys are bytes)
    
    Raises ValueError for invalid input.
    """
    if not data:
        raise ValueError("Empty input")
    
    pos = 0
    result, pos = _bdecode(data, pos)
    
    # Check for trailing data
    if pos != len(data):
        raise ValueError(f"Trailing data after value at position {pos}")
    
    return result


def _bdecode(data: bytes, pos: int):
    """Internal recursive decoder.
    
    Returns (value, new_position)
    """
    if pos >= len(data):
        raise ValueError(f"Unexpected end of data at position {pos}")
    
    c = data[pos:pos+1]
    
    # Integer
    if c == b'i':
        return _decode_int(data, pos)
    
    # List
    elif c == b'l':
        return _decode_list(data, pos)
    
    # Dictionary
    elif c == b'd':
        return _decode_dict(data, pos)
    
    # Bytes/string (must start with digit 0-9)
    elif c in b'0123456789':
        return _decode_bytes(data, pos)
    
    else:
        raise ValueError(f"Unexpected byte {c!r} at position {pos}")


def _decode_int(data: bytes, pos: int):
    """Decode integer starting with 'i'."""
    if data[pos:pos+1] != b'i':
        raise ValueError(f"Expected 'i' at position {pos}")
    
    pos += 1
    start = pos
    
    # Find the 'e'
    while pos < len(data) and data[pos:pos+1] != b'e':
        pos += 1
    
    if pos >= len(data):
        raise ValueError(f"Unterminated integer at position {start}")
    
    # Extract the integer string
    int_str = data[start:pos].decode('ascii')
    
    # Check for empty integer
    if not int_str:
        raise ValueError(f"Empty integer at position {start}")
    
    # Check for leading zeros (except for "0")
    if int_str[0] == '0' and len(int_str) > 1:
        raise ValueError(f"Integer with leading zeros: {int_str}")
    
    # Check for "-0"
    if int_str == '-0':
        raise ValueError(f"Invalid integer: -0")
    
    # Check for bare "-"
    if int_str == '-':
        raise ValueError(f"Invalid integer: bare '-'")
    
    # Parse integer
    try:
        value = int(int_str)
    except ValueError:
        raise ValueError(f"Invalid integer: {int_str}")
    
    # Move past the 'e'
    pos += 1
    
    return value, pos


def _decode_bytes(data: bytes, pos: int):
    """Decode bytes with length prefix."""
    start = pos
    
    # Parse length digits
    while pos < len(data) and data[pos:pos+1] in b'0123456789':
        pos += 1
    
    if pos >= len(data):
        raise ValueError(f"Unterminated length prefix at position {start}")
    
    # Must have a colon
    if data[pos:pos+1] != b':':
        raise ValueError(f"Expected ':' after length at position {pos}")
    
    # Extract length string
    length_str = data[start:pos].decode('ascii')
    
    # Check for empty length
    if not length_str:
        raise ValueError(f"Empty length prefix at position {start}")
    
    # Check for leading zeros (except for "0")
    if length_str[0] == '0' and len(length_str) > 1:
        raise ValueError(f"Length with leading zeros: {length_str}")
    
    # Parse length
    try:
        length = int(length_str)
    except ValueError:
        raise ValueError(f"Invalid length: {length_str}")
    
    # Move past the colon
    pos += 1
    
    # Check if we have enough data
    if pos + length > len(data):
        raise ValueError(f"Insufficient data for string of length {length} at position {pos}")
    
    # Extract the bytes
    value = data[pos:pos+length]
    
    # Move past the bytes
    pos += length
    
    return value, pos


def _decode_list(data: bytes, pos: int):
    """Decode list starting with 'l'."""
    if data[pos:pos+1] != b'l':
        raise ValueError(f"Expected 'l' at position {pos}")
    
    pos += 1
    items = []
    
    while pos < len(data) and data[pos:pos+1] != b'e':
        item, pos = _bdecode(data, pos)
        items.append(item)
    
    if pos >= len(data):
        raise ValueError(f"Unterminated list at position {pos}")
    
    # Move past the 'e'
    pos += 1
    
    return items, pos


def _decode_dict(data: bytes, pos: int):
    """Decode dictionary starting with 'd'."""
    if data[pos:pos+1] != b'd':
        raise ValueError(f"Expected 'd' at position {pos}")
    
    pos += 1
    result = {}
    
    while pos < len(data) and data[pos:pos+1] != b'e':
        # Decode key (must be bytes)
        key, pos = _bdecode(data, pos)
        
        # Check key type
        if not isinstance(key, bytes):
            raise ValueError(f"Dictionary key must be bytes, got {type(key)}")
        
        # Decode value
        value, pos = _bdecode(data, pos)
        
        # Store in dictionary
        result[key] = value
    
    if pos >= len(data):
        raise ValueError(f"Unterminated dictionary at position {pos}")
    
    # Move past the 'e'
    pos += 1
    
    return result, pos