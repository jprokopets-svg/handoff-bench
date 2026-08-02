import json
from typing import Any, Dict, List, Tuple

def encode(obj: Any) -> str:
    """
    Encode a Python object graph to a string, preserving shared references and cycles.
    
    Supported types: int, float, bool, None, str, list, dict (with string keys)
    
    Returns a JSON string representing the object graph with references.
    """
    # Map from object id to reference index
    id_to_ref: Dict[int, int] = {}
    # List of serialized objects
    objects: List[Any] = []
    
    def serialize(obj: Any) -> Any:
        """Serialize an object, handling references and cycles."""
        obj_type = type(obj)
        
        # Handle primitive types that don't need reference tracking
        if obj_type in (int, float, bool, type(None)):
            return {"type": obj_type.__name__, "value": obj}
        
        if obj_type is str:
            return {"type": "str", "value": obj}
        
        # Handle container types (list, dict) - these need reference tracking
        obj_id = id(obj)
        
        if obj_id in id_to_ref:
            # Already seen this object - return a reference
            return {"type": "ref", "ref": id_to_ref[obj_id]}
        
        # Assign a reference number to this object
        ref_num = len(objects)
        id_to_ref[obj_id] = ref_num
        
        if obj_type is list:
            # Create placeholder to handle cycles
            placeholder = {"type": "list", "items": None}
            objects.append(placeholder)
            # Now serialize the items
            items = [serialize(item) for item in obj]
            placeholder["items"] = items
            return {"type": "ref", "ref": ref_num}
        
        elif obj_type is dict:
            # Verify all keys are strings
            for key in obj.keys():
                if not isinstance(key, str):
                    raise ValueError(f"Dict keys must be strings, got {type(key).__name__}")
            
            # Create placeholder to handle cycles
            placeholder = {"type": "dict", "items": None}
            objects.append(placeholder)
            # Now serialize the items
            items = {key: serialize(value) for key, value in obj.items()}
            placeholder["items"] = items
            return {"type": "ref", "ref": ref_num}
        
        else:
            raise ValueError(f"Unsupported type: {obj_type.__name__}")
    
    # Serialize the root object
    root = serialize(obj)
    
    # Build the final structure
    result = {
        "root": root,
        "objects": objects
    }
    
    return json.dumps(result, separators=(',', ':'), ensure_ascii=False)


def decode(s: str) -> Any:
    """
    Decode a string back to a Python object graph, preserving shared references and cycles.
    
    Raises ValueError on malformed input.
    """
    try:
        data = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValueError(f"Malformed JSON: {e}")
    
    if not isinstance(data, dict) or "root" not in data or "objects" not in data:
        raise ValueError("Invalid serialization format: missing 'root' or 'objects'")
    
    root_data = data["root"]
    objects_data = data["objects"]
    
    if not isinstance(objects_data, list):
        raise ValueError("Invalid serialization format: 'objects' must be a list")
    
    # Cache for deserialized objects (by reference index)
    deserialized: Dict[int, Any] = {}
    # Track which objects are being deserialized (to detect cycles during construction)
    in_progress: Dict[int, Any] = {}
    
    def deserialize(obj_data: Any) -> Any:
        """Deserialize an object, handling references and cycles."""
        if not isinstance(obj_data, dict) or "type" not in obj_data:
            raise ValueError("Invalid object data: missing 'type'")
        
        obj_type = obj_data["type"]
        
        if obj_type == "ref":
            if "ref" not in obj_data:
                raise ValueError("Invalid reference: missing 'ref'")
            ref = obj_data["ref"]
            if not isinstance(ref, int) or ref < 0 or ref >= len(objects_data):
                raise ValueError(f"Invalid reference index: {ref}")
            
            if ref in deserialized:
                return deserialized[ref]
            
            if ref in in_progress:
                # We're in a cycle - return the object being constructed
                return in_progress[ref]
            
            # Deserialize the referenced object
            obj_def = objects_data[ref]
            if not isinstance(obj_def, dict) or "type" not in obj_def:
                raise ValueError("Invalid object definition")
            
            obj_type_inner = obj_def["type"]
            
            if obj_type_inner == "list":
                # Create the list first and add to in_progress
                result_list = []
                in_progress[ref] = result_list
                
                if "items" not in obj_def:
                    raise ValueError("Invalid list: missing 'items'")
                items = obj_def["items"]
                if not isinstance(items, list):
                    raise ValueError("Invalid list items: must be a list")
                
                # Deserialize and add items
                for item in items:
                    result_list.append(deserialize(item))
                
                del in_progress[ref]
                deserialized[ref] = result_list
                return result_list
            
            elif obj_type_inner == "dict":
                # Create the dict first and add to in_progress
                result_dict = {}
                in_progress[ref] = result_dict
                
                if "items" not in obj_def:
                    raise ValueError("Invalid dict: missing 'items'")
                items = obj_def["items"]
                if not isinstance(items, dict):
                    raise ValueError("Invalid dict items: must be a dict")
                
                # Deserialize and add items
                for key, value in items.items():
                    result_dict[key] = deserialize(value)
                
                del in_progress[ref]
                deserialized[ref] = result_dict
                return result_dict
            
            else:
                raise ValueError(f"Unknown type in objects: {obj_type_inner}")
        
        elif obj_type == "int":
            if "value" not in obj_data:
                raise ValueError("Invalid int: missing 'value'")
            value = obj_data["value"]
            if not isinstance(value, int) or isinstance(value, bool):
                raise ValueError(f"Invalid int value: {value}")
            return value
        
        elif obj_type == "float":
            if "value" not in obj_data:
                raise ValueError("Invalid float: missing 'value'")
            value = obj_data["value"]
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                raise ValueError(f"Invalid float value: {value}")
            return float(value)
        
        elif obj_type == "bool":
            if "value" not in obj_data:
                raise ValueError("Invalid bool: missing 'value'")
            value = obj_data["value"]
            if not isinstance(value, bool):
                raise ValueError(f"Invalid bool value: {value}")
            return value
        
        elif obj_type == "NoneType":
            if obj_data.get("value") is not None:
                raise ValueError("Invalid None value")
            return None
        
        elif obj_type == "str":
            if "value" not in obj_data:
                raise ValueError("Invalid str: missing 'value'")
            value = obj_data["value"]
            if not isinstance(value, str):
                raise ValueError(f"Invalid str value: {value}")
            return value
        
        else:
            raise ValueError(f"Unknown type: {obj_type}")
    
    return deserialize(root_data)
