def encode(obj: object) -> str:
    """
    Serialize a Python object graph to a string, preserving shared references and cycles.
    Supported types: int, float, bool, None, str, list, dict (string keys only).
    """
    # First pass: assign IDs to all objects
    obj_to_id = {}
    next_id = 0
    stack = [obj]
    
    # BFS to assign IDs to all objects
    while stack:
        current = stack.pop()
        if id(current) in obj_to_id:
            continue
            
        obj_to_id[id(current)] = next_id
        next_id += 1
        
        if isinstance(current, dict):
            for key, value in current.items():
                if not isinstance(key, str):
                    raise ValueError(f"Unsupported dict key type: {type(key)}")
                if isinstance(value, (list, dict)):
                    stack.append(value)
        elif isinstance(current, list):
            for item in current:
                if isinstance(item, (list, dict)):
                    stack.append(item)
    
    # Second pass: serialize with references
    result_parts = []
    
    def serialize(obj_ref):
        obj_id = obj_to_id[id(obj_ref)]
        
        if isinstance(obj_ref, (int, float, bool, type(None), str)):
            # Primitive types
            if isinstance(obj_ref, int):
                return f"i:{obj_ref}:{obj_id}"
            elif isinstance(obj_ref, float):
                return f"f:{obj_ref}:{obj_id}"
            elif isinstance(obj_ref, bool):
                return f"b:{int(obj_ref)}:{obj_id}"
            elif obj_ref is None:
                return f"n::{obj_id}"
            elif isinstance(obj_ref, str):
                # Escape colons and backslashes
                escaped = obj_ref.replace('\\', '\\\\').replace(':', '\\:')
                return f"s:{escaped}:{obj_id}"
        
        elif isinstance(obj_ref, list):
            # List - serialize contents
            item_refs = []
            for item in obj_ref:
                if isinstance(item, (int, float, bool, type(None), str)):
                    # Primitive - serialize inline
                    if isinstance(item, int):
                        item_refs.append(f"i:{item}")
                    elif isinstance(item, float):
                        item_refs.append(f"f:{item}")
                    elif isinstance(item, bool):
                        item_refs.append(f"b:{int(item)}")
                    elif item is None:
                        item_refs.append("n:")
                    elif isinstance(item, str):
                        escaped = item.replace('\\', '\\\\').replace(':', '\\:')
                        item_refs.append(f"s:{escaped}")
                else:
                    # Complex - reference by ID
                    item_refs.append(f"r:{obj_to_id[id(item)]}")
            
            return f"l:{','.join(item_refs)}:{obj_id}"
        
        elif isinstance(obj_ref, dict):
            # Dict - serialize key-value pairs
            pairs = []
            for key, value in obj_ref.items():
                # Key is always a string
                escaped_key = key.replace('\\', '\\\\').replace(':', '\\:')
                
                if isinstance(value, (int, float, bool, type(None), str)):
                    # Primitive value
                    if isinstance(value, int):
                        pairs.append(f"{escaped_key}:i:{value}")
                    elif isinstance(value, float):
                        pairs.append(f"{escaped_key}:f:{value}")
                    elif isinstance(value, bool):
                        pairs.append(f"{escaped_key}:b:{int(value)}")
                    elif value is None:
                        pairs.append(f"{escaped_key}:n:")
                    elif isinstance(value, str):
                        escaped_val = value.replace('\\', '\\\\').replace(':', '\\:')
                        pairs.append(f"{escaped_key}:s:{escaped_val}")
                else:
                    # Complex value - reference by ID
                    pairs.append(f"{escaped_key}:r:{obj_to_id[id(value)]}")
            
            return f"d:{','.join(pairs)}:{obj_id}"
        
        else:
            raise ValueError(f"Unsupported type: {type(obj_ref)}")
    
    # Serialize all objects
    serialized = {}
    for obj_id, obj_ptr in enumerate(obj_to_id.keys()):
        # Find the object with this ID
        for ptr, oid in obj_to_id.items():
            if oid == obj_id:
                obj_ref = None
                # We need to find the actual object
                # Since we only stored IDs, we need to track back to the original
                # Let's do another traversal
                def find_obj(current_obj, target_id):
                    if obj_to_id[id(current_obj)] == target_id:
                        return current_obj
                    
                    if isinstance(current_obj, dict):
                        for k, v in current_obj.items():
                            if isinstance(v, (list, dict)):
                                result = find_obj(v, target_id)
                                if result is not None:
                                    return result
                    elif isinstance(current_obj, list):
                        for item in current_obj:
                            if isinstance(item, (list, dict)):
                                result = find_obj(item, target_id)
                                if result is not None:
                                    return result
                    return None
                
                obj_ref = find_obj(obj, obj_id)
                if obj_ref is not None:
                    serialized[obj_id] = serialize(obj_ref)
                break
    
    # Build final string: all objects separated by '|'
    return '|'.join(serialized[oid] for oid in range(len(serialized)))


def decode(s: str) -> object:
    """
    Deserialize a string back to a Python object graph, preserving shared references and cycles.
    """
    if not s:
        raise ValueError("Empty input string")
    
    parts = s.split('|')
    objects = {}  # id -> object
    unresolved_refs = []  # (obj_id, key_or_index, ref_id)
    
    # First pass: create skeleton objects
    for part in parts:
        if not part:
            continue
            
        # Parse the object
        if part.startswith('i:'):
            # int
            rest = part[2:]
            if ':' not in rest:
                raise ValueError(f"Invalid int format: {part}")
            value_str, id_str = rest.rsplit(':', 1)
            try:
                value = int(value_str)
                obj_id = int(id_str)
            except ValueError:
                raise ValueError(f"Invalid int format: {part}")
            objects[obj_id] = value
            
        elif part.startswith('f:'):
            # float
            rest = part[2:]
            if ':' not in rest:
                raise ValueError(f"Invalid float format: {part}")
            value_str, id_str = rest.rsplit(':', 1)
            try:
                value = float(value_str)
                obj_id = int(id_str)
            except ValueError:
                raise ValueError(f"Invalid float format: {part}")
            objects[obj_id] = value
            
        elif part.startswith('b:'):
            # bool
            rest = part[2:]
            if ':' not in rest:
                raise ValueError(f"Invalid bool format: {part}")
            value_str, id_str = rest.rsplit(':', 1)
            try:
                value = bool(int(value_str))
                obj_id = int(id_str)
            except ValueError:
                raise ValueError(f"Invalid bool format: {part}")
            objects[obj_id] = value
            
        elif part.startswith('n:'):
            # None
            rest = part[2:]
            if ':' not in rest:
                raise ValueError(f"Invalid None format: {part}")
            _, id_str = rest.rsplit(':', 1)
            try:
                obj_id = int(id_str)
            except ValueError:
                raise ValueError(f"Invalid None format: {part}")
            objects[obj_id] = None
            
        elif part.startswith('s:'):
            # string
            rest = part[2:]
            if ':' not in rest:
                raise ValueError(f"Invalid string format: {part}")
            # Need to handle escaped colons
            escaped_str, id_str = rest.rsplit(':', 1)
            # Unescape
            value = escaped_str.replace('\\:', ':').replace('\\\\', '\\')
            try:
                obj_id = int(id_str)
            except ValueError:
                raise ValueError(f"Invalid string format: {part}")
            objects[obj_id] = value
            
        elif part.startswith('l:'):
            # list
            rest = part[2:]
            if ':' not in rest:
                raise ValueError(f"Invalid list format: {part}")
            items_str, id_str = rest.rsplit(':', 1)
            try:
                obj_id = int(id_str)
            except ValueError:
                raise ValueError(f"Invalid list format: {part}")
            
            # Create empty list
            lst = []
            objects[obj_id] = lst
            
            if items_str:
                item_parts = items_str.split(',')
                for i, item_part in enumerate(item_parts):
                    if item_part.startswith('i:'):
                        value = int(item_part[2:])
                        lst.append(value)
                    elif item_part.startswith('f:'):
                        value = float(item_part[2:])
                        lst.append(value)
                    elif item_part.startswith('b:'):
                        value = bool(int(item_part[2:]))
                        lst.append(value)
                    elif item_part == 'n:':
                        lst.append(None)
                    elif item_part.startswith('s:'):
                        escaped = item_part[2:]
                        value = escaped.replace('\\:', ':').replace('\\\\', '\\')
                        lst.append(value)
                    elif item_part.startswith('r:'):
                        ref_id = int(item_part[2:])
                        unresolved_refs.append((obj_id, i, ref_id))
                    else:
                        raise ValueError(f"Invalid list item format: {item_part}")
                        
        elif part.startswith('d:'):
            # dict
            rest = part[2:]
            if ':' not in rest:
                raise ValueError(f"Invalid dict format: {part}")
            pairs_str, id_str = rest.rsplit(':', 1)
            try:
                obj_id = int(id_str)
            except ValueError:
                raise ValueError(f"Invalid dict format: {part}")
            
            # Create empty dict
            dct = {}
            objects[obj_id] = dct
            
            if pairs_str:
                pair_parts = pairs_str.split(',')
                for pair in pair_parts:
                    # Key is always a string, may contain escaped colons
                    # Find the first unescaped colon after the key
                    i = 0
                    while i < len(pair):
                        if pair[i] == '\\':
                            i += 2  # Skip escaped character
                        elif pair[i] == ':':
                            break
                        else:
                            i += 1
                    
                    if i >= len(pair):
                        raise ValueError(f"Invalid dict pair format: {pair}")
                    
                    key_escaped = pair[:i]
                    rest = pair[i+1:]
                    
                    # Unescape key
                    key = key_escaped.replace('\\:', ':').replace('\\\\', '\\')
                    
                    if rest.startswith('i:'):
                        value = int(rest[2:])
                        dct[key] = value
                    elif rest.startswith('f:'):
                        value = float(rest[2:])
                        dct[key] = value
                    elif rest.startswith('b:'):
                        value = bool(int(rest[2:]))
                        dct[key] = value
                    elif rest == 'n:':
                        dct[key] = None
                    elif rest.startswith('s:'):
                        escaped = rest[2:]
                        value = escaped.replace('\\:', ':').replace('\\\\', '\\')
                        dct[key] = value
                    elif rest.startswith('r:'):
                        ref_id = int(rest[2:])
                        unresolved_refs.append((obj_id, key, ref_id))
                    else:
                        raise ValueError(f"Invalid dict value format: {rest}")
                        
        else:
            raise ValueError(f"Unknown object type prefix: {part}")
    
    # Second pass: resolve references
    for obj_id, key_or_index, ref_id in unresolved_refs:
        if ref_id not in objects:
            raise ValueError(f"Reference to non-existent object ID: {ref_id}")
        
        obj = objects[obj_id]
        if isinstance(key_or_index, int):  # list index
            obj[key_or_index] = objects[ref_id]
        else:  # dict key
            obj[key_or_index] = objects[ref_id]
    
    # Return the root object (ID 0)
    if 0 not in objects:
        raise ValueError("No root object (ID 0) found")
    
    return objects[0]