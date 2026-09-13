import json
from typing import Any, Dict, Set

def encode(obj: object) -> str:
    """
    Encode a Python object graph to a string, preserving shared references and cycles.
    
    Supported types: int, float, bool, None, str, list, dict (with string keys)
    
    Returns a JSON string with object IDs to track shared references and cycles.
    """
    # Map from id(obj) to index in objects list
    obj_to_id: Dict[int, int] = {}
    # List of objects in order of first encounter
    objects: list = []
    
    def encode_helper(obj: object) -> Any:
        obj_id = id(obj)
        
        # Handle primitives that don't need reference tracking
        if obj is None or isinstance(obj, bool):
            return {"type": "primitive", "value": obj}
        
        if isinstance(obj, int):
            return {"type": "int", "value": obj}
        
        if isinstance(obj, float):
            return {"type": "float", "value": obj}
        
        if isinstance(obj, str):
            return {"type": "str", "value": obj}
        
        # For container types, track references
        if isinstance(obj, (list, dict)):
            if obj_id in obj_to_id:
                # Already seen this object - return a reference
                return {"type": "ref", "id": obj_to_id[obj_id]}
            
            # First time seeing this object
            idx = len(objects)
            obj_to_id[obj_id] = idx
            
            if isinstance(obj, list):
                # Placeholder to handle cycles
                objects.append(None)
                encoded_list = [encode_helper(item) for item in obj]
                objects[idx] = {"type": "list", "value": encoded_list}
                return {"type": "ref", "id": idx}
            
            elif isinstance(obj, dict):
                # Placeholder to handle cycles
                objects.append(None)
                encoded_dict = {}
                for key, value in obj.items():
                    if not isinstance(key, str):
                        raise ValueError(f"Dict keys must be strings, got {type(key)}")
                    encoded_dict[key] = encode_helper(value)
                objects[idx] = {"type": "dict", "value": encoded_dict}
                return {"type": "ref", "id": idx}
        
        raise ValueError(f"Unsupported type: {type(obj)}")
    
    # Start encoding
    result = encode_helper(obj)
    
    # Package the result with the objects table
    package = {
        "root": result,
        "objects": objects
    }
    
    return json.dumps(package)


def decode(s: str) -> object:
    """
    Decode a string back to a Python object graph, preserving shared references and cycles.
    
    Raises ValueError on malformed input.
    """
    try:
        package = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")
    
    if not isinstance(package, dict) or "root" not in package or "objects" not in package:
        raise ValueError("Invalid package format")
    
    root = package["root"]
    objects_data = package["objects"]
    
    # Cache for decoded objects by index
    decoded_objects: Dict[int, Any] = {}
    
    def decode_helper(encoded: Any) -> object:
        if not isinstance(encoded, dict) or "type" not in encoded:
            raise ValueError("Invalid encoded object")
        
        obj_type = encoded["type"]
        
        if obj_type == "primitive":
            return encoded.get("value")
        
        if obj_type == "int":
            return encoded.get("value")
        
        if obj_type == "float":
            return encoded.get("value")
        
        if obj_type == "str":
            return encoded.get("value")
        
        if obj_type == "ref":
            obj_id = encoded.get("id")
            if not isinstance(obj_id, int) or obj_id < 0 or obj_id >= len(objects_data):
                raise ValueError(f"Invalid reference ID: {obj_id}")
            
            # Check if already decoded
            if obj_id in decoded_objects:
                return decoded_objects[obj_id]
            
            # Decode the object at this index
            obj_data = objects_data[obj_id]
            if obj_data is None:
                raise ValueError(f"Circular reference not yet resolved at index {obj_id}")
            
            if not isinstance(obj_data, dict) or "type" not in obj_data:
                raise ValueError("Invalid object data")
            
            data_type = obj_data["type"]
            
            if data_type == "list":
                # Create list and add to cache before decoding contents (for cycles)
                result_list = []
                decoded_objects[obj_id] = result_list
                
                value = obj_data.get("value")
                if not isinstance(value, list):
                    raise ValueError("Invalid list data")
                
                for item in value:
                    result_list.append(decode_helper(item))
                
                return result_list
            
            elif data_type == "dict":
                # Create dict and add to cache before decoding contents (for cycles)
                result_dict = {}
                decoded_objects[obj_id] = result_dict
                
                value = obj_data.get("value")
                if not isinstance(value, dict):
                    raise ValueError("Invalid dict data")
                
                for key, val in value.items():
                    if not isinstance(key, str):
                        raise ValueError("Dict keys must be strings")
                    result_dict[key] = decode_helper(val)
                
                return result_dict
            
            else:
                raise ValueError(f"Unknown object type: {data_type}")
        
        raise ValueError(f"Unknown encoded type: {obj_type}")
    
    return decode_helper(root)
