import json
from typing import Any, Dict, List, Tuple


def encode(obj: object) -> str:
    """
    Encode a Python object graph to a JSON string, preserving shared references and cycles.
    
    Supported types: int, float, bool, None, str, list, dict (with string keys only)
    
    Returns a JSON string that can be decoded back to an equivalent object structure
    where shared references and cycles are preserved.
    """
    # Track objects by id to detect shared references and cycles
    seen: Dict[int, int] = {}  # Maps object id to reference index
    objects: List[Any] = []    # List of encoded objects
    
    def encode_impl(obj: object) -> Any:
        obj_id = id(obj)
        
        # Handle primitives that don't need reference tracking
        if obj is None or isinstance(obj, bool):
            return {"type": "primitive", "value": obj}
        
        if isinstance(obj, (int, float)):
            return {"type": "primitive", "value": obj}
        
        if isinstance(obj, str):
            return {"type": "primitive", "value": obj}
        
        # For containers, check if we've seen this object before
        if isinstance(obj, (list, dict)):
            if obj_id in seen:
                # Return a reference to the already-encoded object
                return {"type": "ref", "index": seen[obj_id]}
            
            # Mark this object as seen with its index
            ref_index = len(objects)
            seen[obj_id] = ref_index
            
            if isinstance(obj, list):
                # Create placeholder to handle cycles
                placeholder = {"type": "list", "items": None}
                objects.append(placeholder)
                
                # Encode items
                items = [encode_impl(item) for item in obj]
                placeholder["items"] = items
                
                return {"type": "ref", "index": ref_index}
            
            elif isinstance(obj, dict):
                # Validate that all keys are strings
                for key in obj.keys():
                    if not isinstance(key, str):
                        raise ValueError(f"Dict keys must be strings, got {type(key).__name__}")
                
                # Create placeholder to handle cycles
                placeholder = {"type": "dict", "items": None}
                objects.append(placeholder)
                
                # Encode items
                items = {key: encode_impl(value) for key, value in obj.items()}
                placeholder["items"] = items
                
                return {"type": "ref", "index": ref_index}
        
        # Unsupported type
        raise ValueError(f"Unsupported type: {type(obj).__name__}")
    
    # Encode the root object
    root_encoded = encode_impl(obj)
    
    # Build the package
    package = {
        "root": root_encoded,
        "objects": objects
    }
    
    return json.dumps(package)


def decode(s: str) -> object:
    """
    Decode a JSON string back to a Python object graph, preserving shared references and cycles.
    
    Raises ValueError if the input is malformed or contains invalid references.
    """
    try:
        package = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")
    
    if not isinstance(package, dict):
        raise ValueError("Package must be a dict")
    
    if "root" not in package or "objects" not in package:
        raise ValueError("Package must contain 'root' and 'objects' keys")
    
    root_encoded = package["root"]
    objects_data = package["objects"]
    
    if not isinstance(objects_data, list):
        raise ValueError("'objects' must be a list")
    
    # Cache for decoded objects to preserve identity
    decoded_cache: Dict[int, Any] = {}
    
    def decode_impl(encoded: Any) -> Any:
        if not isinstance(encoded, dict):
            raise ValueError("Encoded value must be a dict")
        
        if "type" not in encoded:
            raise ValueError("Encoded value must have 'type' key")
        
        enc_type = encoded["type"]
        
        if enc_type == "primitive":
            if "value" not in encoded:
                raise ValueError("Primitive must have 'value' key")
            return encoded["value"]
        
        elif enc_type == "ref":
            if "index" not in encoded:
                raise ValueError("Reference must have 'index' key")
            
            ref_index = encoded["index"]
            if not isinstance(ref_index, int) or ref_index < 0 or ref_index >= len(objects_data):
                raise ValueError(f"Invalid reference index: {ref_index}")
            
            # Check if already decoded
            if ref_index in decoded_cache:
                return decoded_cache[ref_index]
            
            obj_data = objects_data[ref_index]
            if not isinstance(obj_data, dict):
                raise ValueError(f"Object at index {ref_index} must be a dict")
            
            if "type" not in obj_data:
                raise ValueError(f"Object at index {ref_index} must have 'type' key")
            
            obj_type = obj_data["type"]
            
            if obj_type == "list":
                if "items" not in obj_data:
                    raise ValueError(f"List object at index {ref_index} must have 'items' key")
                
                # Create the list first and cache it to handle cycles
                result_list: List[Any] = []
                decoded_cache[ref_index] = result_list
                
                # Now decode and populate items
                items = obj_data["items"]
                if not isinstance(items, list):
                    raise ValueError(f"List items must be a list")
                
                for item_encoded in items:
                    result_list.append(decode_impl(item_encoded))
                
                return result_list
            
            elif obj_type == "dict":
                if "items" not in obj_data:
                    raise ValueError(f"Dict object at index {ref_index} must have 'items' key")
                
                # Create the dict first and cache it to handle cycles
                result_dict: Dict[str, Any] = {}
                decoded_cache[ref_index] = result_dict
                
                # Now decode and populate items
                items = obj_data["items"]
                if not isinstance(items, dict):
                    raise ValueError(f"Dict items must be a dict")
                
                for key, value_encoded in items.items():
                    if not isinstance(key, str):
                        raise ValueError(f"Dict key must be string, got {type(key).__name__}")
                    result_dict[key] = decode_impl(value_encoded)
                
                return result_dict
            
            else:
                raise ValueError(f"Unknown object type: {obj_type}")
        
        else:
            raise ValueError(f"Unknown encoded type: {enc_type}")
    
    return decode_impl(root_encoded)
