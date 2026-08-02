import json
from typing import Any, Dict, List, Union

def encode(obj: object) -> str:
    """Serialize object graph to string, preserving shared references and cycles."""
    # Track objects we've seen and their IDs
    obj_to_id: Dict[int, int] = {}
    next_id = 0
    
    def _encode(obj: Any) -> Any:
        nonlocal next_id
        
        # Handle None, bool, int, float, str
        if obj is None:
            return {"$type": "null"}
        elif isinstance(obj, bool):
            return {"$type": "bool", "value": obj}
        elif isinstance(obj, int):
            return {"$type": "int", "value": obj}
        elif isinstance(obj, float):
            return {"$type": "float", "value": obj}
        elif isinstance(obj, str):
            return {"$type": "str", "value": obj}
        
        # For containers (list, dict), check if we've seen this object before
        obj_id = id(obj)
        if obj_id in obj_to_id:
            return {"$type": "ref", "id": obj_to_id[obj_id]}
        
        # Assign ID to this object
        obj_to_id[obj_id] = next_id
        current_id = next_id
        next_id += 1
        
        if isinstance(obj, list):
            # Create placeholder first
            result = {"$type": "list", "id": current_id, "items": []}
            # Encode items
            result["items"] = [_encode(item) for item in obj]
            return result
        elif isinstance(obj, dict):
            # Check keys are strings
            for key in obj.keys():
                if not isinstance(key, str):
                    raise ValueError("Dict keys must be strings")
            # Create placeholder first
            result = {"$type": "dict", "id": current_id, "items": {}}
            # Encode items
            result["items"] = {key: _encode(value) for key, value in obj.items()}
            return result
        else:
            raise ValueError(f"Unsupported type: {type(obj)}")
    
    encoded = _encode(obj)
    return json.dumps(encoded, ensure_ascii=False)

def decode(s: str) -> object:
    """Deserialize string back to object graph, preserving shared references and cycles."""
    try:
        data = json.loads(s)
    except json.JSONDecodeError:
        raise ValueError("Malformed JSON input")
    
    # Track objects by ID for reconstruction
    id_to_obj: Dict[int, Any] = {}
    
    def _decode(obj_data: Any) -> Any:
        if not isinstance(obj_data, dict) or "$type" not in obj_data:
            raise ValueError("Invalid encoded object")
        
        obj_type = obj_data["$type"]
        
        if obj_type == "null":
            return None
        elif obj_type == "bool":
            return bool(obj_data["value"])
        elif obj_type == "int":
            return int(obj_data["value"])
        elif obj_type == "float":
            return float(obj_data["value"])
        elif obj_type == "str":
            return str(obj_data["value"])
        elif obj_type == "ref":
            ref_id = obj_data["id"]
            if ref_id not in id_to_obj:
                raise ValueError(f"Reference to undefined object ID: {ref_id}")
            return id_to_obj[ref_id]
        elif obj_type == "list":
            if "id" not in obj_data or "items" not in obj_data:
                raise ValueError("Invalid list encoding")
            
            list_id = obj_data["id"]
            # Create empty list as placeholder
            lst = []
            id_to_obj[list_id] = lst
            
            # Decode items
            items_data = obj_data["items"]
            if not isinstance(items_data, list):
                raise ValueError("Invalid list items encoding")
            
            lst.extend(_decode(item) for item in items_data)
            return lst
        elif obj_type == "dict":
            if "id" not in obj_data or "items" not in obj_data:
                raise ValueError("Invalid dict encoding")
            
            dict_id = obj_data["id"]
            # Create empty dict as placeholder
            dct = {}
            id_to_obj[dict_id] = dct
            
            # Decode items
            items_data = obj_data["items"]
            if not isinstance(items_data, dict):
                raise ValueError("Invalid dict items encoding")
            
            for key, value_data in items_data.items():
                if not isinstance(key, str):
                    raise ValueError("Dict key must be string")
                dct[key] = _decode(value_data)
            return dct
        else:
            raise ValueError(f"Unknown type: {obj_type}")
    
    return _decode(data)