import json


def encode(obj: object) -> str:
    """
    Encode a Python object to a JSON string, preserving shared references and cycles.
    
    Format:
    - Primitives (None, bool, int, float, str) are encoded directly
    - Containers (list, dict) are assigned unique IDs and stored in a registry
    - References to containers use {"__ref__": id} format
    - Cycles are handled by pre-assigning IDs before encoding contents
    """
    seen = {}  # Maps id(obj) -> assigned_id
    containers = {}  # Maps assigned_id -> encoded container
    next_id = [0]  # Use list to allow modification in nested function
    in_progress = set()  # Track objects currently being encoded (cycle detection)
    
    def encode_value(val):
        # Handle primitives
        if val is None or isinstance(val, bool):
            return val
        if isinstance(val, (int, float)):
            return val
        if isinstance(val, str):
            return val
        
        # Handle containers
        if isinstance(val, (list, dict)):
            obj_id = id(val)
            
            # If already seen, return reference
            if obj_id in seen:
                return {"__ref__": seen[obj_id]}
            
            # Detect cycles
            if obj_id in in_progress:
                # Assign ID if not already assigned
                if obj_id not in seen:
                    assigned_id = next_id[0]
                    next_id[0] += 1
                    seen[obj_id] = assigned_id
                return {"__ref__": seen[obj_id]}
            
            # Assign ID to this container
            assigned_id = next_id[0]
            next_id[0] += 1
            seen[obj_id] = assigned_id
            in_progress.add(obj_id)
            
            try:
                if isinstance(val, list):
                    encoded = [encode_value(item) for item in val]
                    containers[assigned_id] = {"__list__": encoded}
                else:  # dict
                    encoded = {k: encode_value(v) for k, v in val.items()}
                    containers[assigned_id] = {"__dict__": encoded}
            finally:
                in_progress.remove(obj_id)
            
            return {"__ref__": assigned_id}
        
        # Unsupported type
        raise ValueError(f"Unsupported type: {type(val)}")
    
    # Encode the root object
    root = encode_value(obj)
    
    # Build the final structure
    result = {
        "root": root,
        "containers": containers
    }
    
    return json.dumps(result)


def decode(s: str) -> object:
    """
    Decode a JSON string back to a Python object, restoring shared references and cycles.
    
    Uses a two-pass approach:
    1. Pre-create all container objects and cache them by ID
    2. Populate container contents, which may reference other containers or themselves
    """
    try:
        data = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValueError(f"Malformed JSON: {e}")
    
    if not isinstance(data, dict) or "root" not in data or "containers" not in data:
        raise ValueError("Invalid encoded format: missing 'root' or 'containers'")
    
    root_data = data["root"]
    containers_data = data["containers"]
    
    # Validate containers_data is a dict
    if not isinstance(containers_data, dict):
        raise ValueError("Invalid encoded format: 'containers' must be a dict")
    
    obj_cache = {}  # Maps assigned_id -> actual object
    
    # First pass: create all container objects (empty)
    for id_str, container_info in containers_data.items():
        try:
            assigned_id = int(id_str)
        except ValueError:
            raise ValueError(f"Invalid container ID: {id_str}")
        
        if not isinstance(container_info, dict):
            raise ValueError(f"Container info must be a dict, got {type(container_info)}")
        
        if "__list__" in container_info:
            obj_cache[assigned_id] = []
        elif "__dict__" in container_info:
            obj_cache[assigned_id] = {}
        else:
            raise ValueError(f"Unknown container type in: {container_info}")
    
    # Second pass: populate container contents
    for id_str, container_info in containers_data.items():
        assigned_id = int(id_str)
        obj = obj_cache[assigned_id]
        
        if "__list__" in container_info:
            items = container_info["__list__"]
            if not isinstance(items, list):
                raise ValueError(f"List contents must be a list, got {type(items)}")
            for item in items:
                obj.append(decode_value(item, obj_cache))
        elif "__dict__" in container_info:
            items = container_info["__dict__"]
            if not isinstance(items, dict):
                raise ValueError(f"Dict contents must be a dict, got {type(items)}")
            for k, v in items.items():
                if not isinstance(k, str):
                    raise ValueError(f"Dict keys must be strings, got {type(k)}")
                obj[k] = decode_value(v, obj_cache)
    
    # Decode the root value
    return decode_value(root_data, obj_cache)


def decode_value(val, obj_cache):
    """Helper to decode a single value, resolving references."""
    if val is None or isinstance(val, bool):
        return val
    if isinstance(val, (int, float)):
        return val
    if isinstance(val, str):
        return val
    if isinstance(val, dict):
        if "__ref__" in val:
            ref_id = val["__ref__"]
            if not isinstance(ref_id, int):
                raise ValueError(f"Reference ID must be int, got {type(ref_id)}")
            if ref_id not in obj_cache:
                raise ValueError(f"Reference to unknown object ID: {ref_id}")
            return obj_cache[ref_id]
        raise ValueError(f"Unknown dict format: {val}")
    raise ValueError(f"Cannot decode value of type {type(val)}: {val}")
