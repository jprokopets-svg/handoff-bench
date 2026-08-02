import json
from typing import Any, Dict, Set, Tuple


def encode(obj: object) -> str:
    """
    Serialize a Python object graph to a JSON string, preserving shared references and cycles.
    
    Supported types: int, float, bool, None, str, list, dict (with string keys only).
    
    Raises ValueError if obj contains an unsupported type.
    """
    seen = {}  # Maps id(obj) -> index in objects array
    objects = []  # Array of serialized objects
    
    def serialize(o: object) -> Any:
        # Handle primitives that don't need reference tracking
        if o is None or isinstance(o, bool):
            return {'type': 'bool' if isinstance(o, bool) else 'none', 'value': o}
        if isinstance(o, int):
            return {'type': 'int', 'value': o}
        if isinstance(o, float):
            return {'type': 'float', 'value': o}
        if isinstance(o, str):
            return {'type': 'str', 'value': o}
        
        # For containers, check if we've seen this object before
        obj_id = id(o)
        if obj_id in seen:
            return {'type': 'ref', 'index': seen[obj_id]}
        
        # Mark as in-progress to detect cycles
        seen[obj_id] = len(objects)
        placeholder_index = len(objects)
        objects.append(None)  # Placeholder
        
        if isinstance(o, list):
            serialized = {
                'type': 'list',
                'value': [serialize(item) for item in o]
            }
        elif isinstance(o, dict):
            # Validate that all keys are strings
            for key in o.keys():
                if not isinstance(key, str):
                    raise ValueError(f"Dict keys must be strings, got {type(key).__name__}")
            serialized = {
                'type': 'dict',
                'value': {key: serialize(val) for key, val in o.items()}
            }
        else:
            raise ValueError(f"Unsupported type: {type(o).__name__}")
        
        objects[placeholder_index] = serialized
        return {'type': 'ref', 'index': placeholder_index}
    
    root = serialize(obj)
    return json.dumps({'root': root, 'objects': objects})


def decode(s: str) -> object:
    """
    Deserialize a JSON string back to a Python object graph, preserving shared references and cycles.
    
    Raises ValueError if the input is malformed or contains invalid data.
    """
    try:
        data = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")
    
    if not isinstance(data, dict) or 'root' not in data or 'objects' not in data:
        raise ValueError("Invalid serialization format: missing 'root' or 'objects'")
    
    root_data = data['root']
    objects_data = data['objects']
    
    if not isinstance(objects_data, list):
        raise ValueError("Invalid serialization format: 'objects' must be an array")
    
    # Cache for deserialized objects
    cache = {}
    in_progress = set()  # Track objects being deserialized to handle cycles
    
    def deserialize(obj_data: Any) -> object:
        if not isinstance(obj_data, dict) or 'type' not in obj_data:
            raise ValueError("Invalid object data: missing 'type'")
        
        obj_type = obj_data['type']
        
        if obj_type == 'none':
            return None
        elif obj_type == 'bool':
            if 'value' not in obj_data:
                raise ValueError("Invalid bool data: missing 'value'")
            val = obj_data['value']
            if not isinstance(val, bool):
                raise ValueError(f"Invalid bool value: {val}")
            return val
        elif obj_type == 'int':
            if 'value' not in obj_data:
                raise ValueError("Invalid int data: missing 'value'")
            val = obj_data['value']
            if not isinstance(val, int) or isinstance(val, bool):
                raise ValueError(f"Invalid int value: {val}")
            return val
        elif obj_type == 'float':
            if 'value' not in obj_data:
                raise ValueError("Invalid float data: missing 'value'")
            val = obj_data['value']
            if not isinstance(val, (int, float)) or isinstance(val, bool):
                raise ValueError(f"Invalid float value: {val}")
            return float(val)
        elif obj_type == 'str':
            if 'value' not in obj_data:
                raise ValueError("Invalid str data: missing 'value'")
            val = obj_data['value']
            if not isinstance(val, str):
                raise ValueError(f"Invalid str value: {val}")
            return val
        elif obj_type == 'ref':
            if 'index' not in obj_data:
                raise ValueError("Invalid ref data: missing 'index'")
            index = obj_data['index']
            if not isinstance(index, int) or index < 0 or index >= len(objects_data):
                raise ValueError(f"Invalid ref index: {index}")
            
            if index in cache:
                return cache[index]
            
            if index in in_progress:
                # Cycle detected - create placeholder and return it
                # The actual object will be filled in when we finish deserializing
                if index not in cache:
                    # For lists and dicts, we need to create the container first
                    obj_def = objects_data[index]
                    if obj_def['type'] == 'list':
                        cache[index] = []
                    elif obj_def['type'] == 'dict':
                        cache[index] = {}
                return cache[index]
            
            in_progress.add(index)
            obj_def = objects_data[index]
            
            if not isinstance(obj_def, dict) or 'type' not in obj_def:
                raise ValueError(f"Invalid object definition at index {index}")
            
            obj_type_inner = obj_def['type']
            
            if obj_type_inner == 'list':
                if 'value' not in obj_def:
                    raise ValueError(f"Invalid list data at index {index}: missing 'value'")
                result = []
                cache[index] = result
                for item_data in obj_def['value']:
                    result.append(deserialize(item_data))
            elif obj_type_inner == 'dict':
                if 'value' not in obj_def:
                    raise ValueError(f"Invalid dict data at index {index}: missing 'value'")
                result = {}
                cache[index] = result
                for key, val_data in obj_def['value'].items():
                    if not isinstance(key, str):
                        raise ValueError(f"Invalid dict key type at index {index}: {type(key).__name__}")
                    result[key] = deserialize(val_data)
            else:
                raise ValueError(f"Invalid object type in objects array: {obj_type_inner}")
            
            in_progress.discard(index)
            return cache[index]
        else:
            raise ValueError(f"Unknown type: {obj_type}")
    
    return deserialize(root_data)
