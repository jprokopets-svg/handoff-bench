"""
Graph serializer that preserves shared references and cycles.
"""

import json
from typing import Any


def encode(obj: Any) -> str:
    """
    Encode a Python object to a string, preserving shared references and cycles.
    
    Supported types: int, float, bool, None, str, list, dict (with string keys)
    
    Raises ValueError if an unsupported type is encountered.
    """
    # Track objects we've already seen by id
    seen = {}
    # Counter for object IDs in the serialization
    obj_counter = [0]
    # Track objects currently being encoded (for cycle detection)
    in_progress = set()
    
    def get_obj_id(obj_id: int) -> int:
        """Get or create a serialization ID for an object."""
        if obj_id not in seen:
            seen[obj_id] = obj_counter[0]
            obj_counter[0] += 1
        return seen[obj_id]
    
    def encode_impl(obj: Any) -> Any:
        """Recursively encode an object."""
        obj_type = type(obj)
        
        # Handle primitive types
        if obj is None or isinstance(obj, (bool, int, float, str)):
            return {"type": obj_type.__name__, "value": obj}
        
        # Handle list
        if isinstance(obj, list):
            obj_id = id(obj)
            ref_id = get_obj_id(obj_id)
            
            # If we're already encoding this object, return a reference
            if obj_id in in_progress:
                return {"type": "ref", "id": ref_id}
            
            in_progress.add(obj_id)
            try:
                result = {
                    "type": "list",
                    "id": ref_id,
                    "value": [encode_impl(item) for item in obj]
                }
            finally:
                in_progress.discard(obj_id)
            return result
        
        # Handle dict
        if isinstance(obj, dict):
            obj_id = id(obj)
            ref_id = get_obj_id(obj_id)
            
            # If we're already encoding this object, return a reference
            if obj_id in in_progress:
                return {"type": "ref", "id": ref_id}
            
            in_progress.add(obj_id)
            try:
                result = {
                    "type": "dict",
                    "id": ref_id,
                    "value": {k: encode_impl(v) for k, v in obj.items()}
                }
            finally:
                in_progress.discard(obj_id)
            return result
        
        # Unsupported type
        raise ValueError(f"Unsupported type: {obj_type.__name__}")
    
    encoded = encode_impl(obj)
    return json.dumps(encoded)


def decode(s: str) -> Any:
    """
    Decode a string back to a Python object, preserving shared references and cycles.
    
    Raises ValueError if the input is malformed.
    """
    try:
        encoded = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValueError(f"Malformed JSON: {e}")
    
    # Track decoded objects by their reference ID
    obj_cache = {}
    
    def decode_impl(encoded: Any) -> Any:
        """Recursively decode an object."""
        if not isinstance(encoded, dict):
            raise ValueError("Invalid encoded format")
        
        obj_type = encoded.get("type")
        
        if obj_type is None:
            raise ValueError("Missing 'type' field")
        
        # Handle primitive types
        if obj_type in ("NoneType", "bool", "int", "float", "str"):
            if "value" not in encoded:
                raise ValueError(f"Missing 'value' field for type {obj_type}")
            return encoded["value"]
        
        # Handle reference
        if obj_type == "ref":
            if "id" not in encoded:
                raise ValueError("Missing 'id' field for ref")
            ref_id = encoded["id"]
            if ref_id not in obj_cache:
                raise ValueError(f"Reference to unknown object: {ref_id}")
            return obj_cache[ref_id]
        
        # Handle list
        if obj_type == "list":
            if "id" not in encoded or "value" not in encoded:
                raise ValueError("Missing 'id' or 'value' field for list")
            
            ref_id = encoded["id"]
            
            # Check if we've already started decoding this object (cycle detection)
            if ref_id in obj_cache:
                return obj_cache[ref_id]
            
            # Create the list and cache it before decoding items (for cycle support)
            result = []
            obj_cache[ref_id] = result
            
            # Decode items
            for item_encoded in encoded["value"]:
                result.append(decode_impl(item_encoded))
            
            return result
        
        # Handle dict
        if obj_type == "dict":
            if "id" not in encoded or "value" not in encoded:
                raise ValueError("Missing 'id' or 'value' field for dict")
            
            ref_id = encoded["id"]
            
            # Check if we've already started decoding this object (cycle detection)
            if ref_id in obj_cache:
                return obj_cache[ref_id]
            
            # Create the dict and cache it before decoding items (for cycle support)
            result = {}
            obj_cache[ref_id] = result
            
            # Decode items
            for k, v_encoded in encoded["value"].items():
                result[k] = decode_impl(v_encoded)
            
            return result
        
        raise ValueError(f"Unknown type: {obj_type}")
    
    return decode_impl(encoded)
