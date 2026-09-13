def encode(obj: object) -> str:
    """Serialize object graph to string preserving shared references and cycles."""
    from typing import Any, Dict, List, Union
    
    # Supported types: int, float, bool, None, str, list, dict with string keys
    def check_type(o: Any) -> None:
        if o is None:
            return
        if isinstance(o, (int, float, bool, str)):
            return
        if isinstance(o, list):
            for item in o:
                check_type(item)
            return
        if isinstance(o, dict):
            for key, value in o.items():
                if not isinstance(key, str):
                    raise ValueError(f"Unsupported dict key type: {type(key)}")
                check_type(value)
            return
        raise ValueError(f"Unsupported type: {type(o)}")
    
    check_type(obj)
    
    # Serialization state
    next_id = 0
    obj_to_id: Dict[int, int] = {}  # id(obj) -> serial id
    id_to_obj: Dict[int, Any] = {}  # serial id -> object
    result_parts: List[str] = []
    
    def encode_value(o: Any) -> str:
        nonlocal next_id
        if o is None:
            return "null"
        if isinstance(o, bool):
            return "true" if o else "false"
        if isinstance(o, int):
            return str(o)
        if isinstance(o, float):
            # Handle infinity, nan if needed
            if o == float('inf'):
                return "Infinity"
            if o == float('-inf'):
                return "-Infinity"
            if o != o:  # nan
                return "NaN"
            return repr(o)  # Use repr for exact representation
        if isinstance(o, str):
            # Escape quotes and backslashes
            escaped = o.replace('\\', '\\\\').replace('"', '\\"')
            return f'"{escaped}"'
        
        # For containers, check if we've seen this object before
        obj_id = id(o)
        if obj_id in obj_to_id:
            # Reference to previously seen object
            return f'@ref{obj_to_id[obj_id]}'
        
        # New object - assign ID
        serial_id = next_id
        next_id += 1
        obj_to_id[obj_id] = serial_id
        id_to_obj[serial_id] = o
        
        if isinstance(o, list):
            items = [encode_value(item) for item in o]
            return f'@list{serial_id}[{",".join(items)}]'
        elif isinstance(o, dict):
            items = []
            for key, value in sorted(o.items()):  # Sort for deterministic output
                items.append(f'{encode_value(key)}:{encode_value(value)}')
            return f'@dict{serial_id}{{{",".join(items)}}}'
        else:
            # Should not reach here due to check_type
            raise ValueError(f"Unsupported type: {type(o)}")
    
    result = encode_value(obj)
    return result


def decode(s: str) -> object:
    """Deserialize string back to object graph preserving shared references and cycles."""
    from typing import Any, Dict, List
    
    if not s:
        raise ValueError("Empty string")
    
    # State for reconstruction
    id_to_obj: Dict[int, Any] = {}
    
    def parse_value(start: int) -> tuple[Any, int]:
        """Parse a value starting at position start, return (value, next_position)."""
        nonlocal id_to_obj
        
        if s[start] == 'n':  # null
            if s[start:start+4] == 'null':
                return None, start + 4
            raise ValueError(f"Invalid token at position {start}")
        
        if s[start] == 't':  # true
            if s[start:start+4] == 'true':
                return True, start + 4
            raise ValueError(f"Invalid token at position {start}")
        
        if s[start] == 'f':  # false
            if s[start:start+5] == 'false':
                return False, start + 5
            raise ValueError(f"Invalid token at position {start}")
        
        if s[start] == '"':  # string
            end = start + 1
            while end < len(s):
                if s[end] == '"' and s[end-1] != '\\':
                    break
                end += 1
            if end >= len(s) or s[end] != '"':
                raise ValueError(f"Unterminated string at position {start}")
            escaped = s[start+1:end]
            # Unescape
            result = []
            i = 0
            while i < len(escaped):
                if escaped[i] == '\\':
                    if i+1 >= len(escaped):
                        raise ValueError(f"Invalid escape at position {start+i+1}")
                    result.append(escaped[i+1])
                    i += 2
                else:
                    result.append(escaped[i])
                    i += 1
            return ''.join(result), end + 1
        
        if s[start] == '@':  # reference or container
            start += 1  # Skip '@'
            
            # Check if it's a reference
            if s.startswith('ref', start):
                # Parse reference ID
                start += 3  # Skip 'ref'
                end = start
                while end < len(s) and s[end].isdigit():
                    end += 1
                if end == start:
                    raise ValueError(f"Missing reference ID at position {start}")
                
                ref_id = int(s[start:end])
                if ref_id in id_to_obj:
                    return id_to_obj[ref_id], end
                else:
                    raise ValueError(f"Forward reference to id {ref_id}")
            
            # Check if it's a list
            elif s.startswith('list', start):
                start += 4  # Skip 'list'
                end = start
                while end < len(s) and s[end].isdigit():
                    end += 1
                if end == start:
                    raise ValueError(f"Missing list ID at position {start}")
                
                list_id = int(s[start:end])
                
                if s[end] != '[':
                    raise ValueError(f"Expected '[' after list ID at position {end}")
                end += 1
                
                # Create empty list first to handle cycles
                lst = []
                id_to_obj[list_id] = lst
                
                # Parse items
                if s[end] == ']':
                    return lst, end + 1
                
                while True:
                    item, end = parse_value(end)
                    lst.append(item)
                    
                    if end >= len(s):
                        raise ValueError(f"Unterminated list at position {start}")
                    
                    if s[end] == ']':
                        return lst, end + 1
                    elif s[end] == ',':
                        end += 1
                    else:
                        raise ValueError(f"Expected ',' or ']' at position {end}")
            
            # Check if it's a dict
            elif s.startswith('dict', start):
                start += 4  # Skip 'dict'
                end = start
                while end < len(s) and s[end].isdigit():
                    end += 1
                if end == start:
                    raise ValueError(f"Missing dict ID at position {start}")
                
                dict_id = int(s[start:end])
                
                if s[end] != '{':
                    raise ValueError(f"Expected '{{' after dict ID at position {end}")
                end += 1
                
                # Create empty dict first to handle cycles
                dct = {}
                id_to_obj[dict_id] = dct
                
                if s[end] == '}':
                    return dct, end + 1
                
                while True:
                    # Parse key
                    key, end = parse_value(end)
                    if not isinstance(key, str):
                        raise ValueError(f"Dict key must be string, got {type(key)}")
                    
                    if end >= len(s) or s[end] != ':':
                        raise ValueError(f"Expected ':' after dict key at position {end}")
                    end += 1
                    
                    # Parse value
                    value, end = parse_value(end)
                    dct[key] = value
                    
                    if end >= len(s):
                        raise ValueError(f"Unterminated dict at position {start}")
                    
                    if s[end] == '}':
                        return dct, end + 1
                    elif s[end] == ',':
                        end += 1
                    else:
                        raise ValueError(f"Expected ',' or '}}' at position {end}")
            
            else:
                raise ValueError(f"Unknown container type at position {start}")
        
        # Number (int or float)
        # Parse number
        end = start
        while end < len(s) and (s[end].isdigit() or s[end] in '.-+eE'):
            end += 1
        
        num_str = s[start:end]
        if not num_str:
            raise ValueError(f"Invalid token at position {start}")
        
        # Try int first, then float
        if '.' in num_str or 'e' in num_str or 'E' in num_str or num_str in ('Infinity', '-Infinity', 'NaN'):
            if num_str == 'Infinity':
                return float('inf'), end
            if num_str == '-Infinity':
                return float('-inf'), end
            if num_str == 'NaN':
                return float('nan'), end
            try:
                return float(num_str), end
            except ValueError:
                raise ValueError(f"Invalid float literal: {num_str}")
        else:
            try:
                return int(num_str), end
            except ValueError:
                raise ValueError(f"Invalid int literal: {num_str}")
    
    try:
        result, pos = parse_value(0)
        if pos != len(s):
            raise ValueError(f"Extra characters after parsed value at position {pos}")
        return result
    except (ValueError, IndexError) as e:
        raise ValueError(f"Malformed input: {e}")