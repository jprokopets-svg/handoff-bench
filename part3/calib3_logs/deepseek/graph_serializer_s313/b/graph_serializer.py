import json
from typing import Any, Dict, List

def encode(obj: object) -> str:
    """Serialize object graph to string, preserving shared references and cycles."""
    # Maps from object id to index in the objects list
    obj_to_idx: Dict[int, int] = {}
    # List of objects in order of first encounter
    objects: List[Any] = []
    # Result structure that will be JSON serialized
    result: List[Any] = []
    
    def _encode(obj: Any) -> Any:
        # Handle primitive types directly
        if obj is None:
            return [3]  # type code for None
        elif isinstance(obj, bool):
            return [2, obj]  # type code for bool
        elif isinstance(obj, int):
            return [0, obj]  # type code for int
        elif isinstance(obj, float):
            return [1, obj]  # type code for float
        elif isinstance(obj, str):
            return [4, obj]  # type code for str
        elif isinstance(obj, list):
            obj_id = id(obj)
            if obj_id in obj_to_idx:
                # Already seen - return reference
                return [7, obj_to_idx[obj_id]]  # type code for reference
            
            # First time seeing this list
            idx = len(objects)
            obj_to_idx[obj_id] = idx
            objects.append(obj)
            
            # Create placeholder in result
            result_idx = len(result)
            result.append(None)  # Placeholder
            
            # Encode contents
            encoded_contents = [_encode(item) for item in obj]
            
            # Update result with actual encoded list
            result[result_idx] = [5, encoded_contents]  # type code for list
            return [7, idx]  # Return reference
        
        elif isinstance(obj, dict):
            # Check that all keys are strings
            for key in obj.keys():
                if not isinstance(key, str):
                    raise ValueError(f"Dict key must be str, got {type(key)}")
            
            obj_id = id(obj)
            if obj_id in obj_to_idx:
                # Already seen - return reference
                return [7, obj_to_idx[obj_id]]  # type code for reference
            
            # First time seeing this dict
            idx = len(objects)
            obj_to_idx[obj_id] = idx
            objects.append(obj)
            
            # Create placeholder in result
            result_idx = len(result)
            result.append(None)  # Placeholder
            
            # Encode contents
            encoded_contents = []
            for key, value in obj.items():
                encoded_contents.append([key, _encode(value)])
            
            # Update result with actual encoded dict
            result[result_idx] = [6, encoded_contents]  # type code for dict
            return [7, idx]  # Return reference
        
        else:
            raise ValueError(f"Unsupported type: {type(obj)}")
    
    # Start encoding
    _encode(obj)
    
    # Build final structure: [objects, root_reference]
    # The root object is always at index 0 in objects
    return json.dumps([result, 0])

def decode(s: str) -> object:
    """Deserialize string back to object graph, preserving shared references and cycles."""
    try:
        data = json.loads(s)
    except json.JSONDecodeError:
        raise ValueError("Malformed JSON input")
    
    if not isinstance(data, list) or len(data) != 2:
        raise ValueError("Invalid encoded format")
    
    objects_data, root_idx = data
    if not isinstance(objects_data, list):
        raise ValueError("Invalid objects data")
    if not isinstance(root_idx, int):
        raise ValueError("Invalid root index")
    
    # Cache for already decoded objects
    decoded_objects: List[Any] = []
    
    def _decode_item(item: Any) -> Any:
        """Decode a single encoded item (could be primitive or reference)."""
        if not isinstance(item, list) or len(item) < 1:
            raise ValueError("Invalid encoded item")
        
        type_code = item[0]
        
        if type_code == 0:  # int
            if len(item) != 2 or not isinstance(item[1], int):
                raise ValueError("Invalid int encoding")
            return item[1]
        elif type_code == 1:  # float
            if len(item) != 2 or not isinstance(item[1], (int, float)):
                raise ValueError("Invalid float encoding")
            return float(item[1])
        elif type_code == 2:  # bool
            if len(item) != 2 or not isinstance(item[1], bool):
                raise ValueError("Invalid bool encoding")
            return item[1]
        elif type_code == 3:  # None
            if len(item) != 1:
                raise ValueError("Invalid None encoding")
            return None
        elif type_code == 4:  # str
            if len(item) != 2 or not isinstance(item[1], str):
                raise ValueError("Invalid str encoding")
            return item[1]
        elif type_code == 5:  # list
            if len(item) != 2 or not isinstance(item[1], list):
                raise ValueError("Invalid list encoding")
            
            # Create list and store in cache immediately to handle cycles
            lst = []
            idx = len(decoded_objects)
            decoded_objects.append(lst)
            
            # Decode contents
            for encoded_item in item[1]:
                lst.append(_decode_item(encoded_item))
            
            return lst
        elif type_code == 6:  # dict
            if len(item) != 2 or not isinstance(item[1], list):
                raise ValueError("Invalid dict encoding")
            
            # Create dict and store in cache immediately to handle cycles
            dct = {}
            idx = len(decoded_objects)
            decoded_objects.append(dct)
            
            # Decode contents
            for pair in item[1]:
                if not isinstance(pair, list) or len(pair) != 2:
                    raise ValueError("Invalid dict pair encoding")
                key, encoded_value = pair
                if not isinstance(key, str):
                    raise ValueError("Dict key must be str")
                dct[key] = _decode_item(encoded_value)
            
            return dct
        elif type_code == 7:  # reference
            if len(item) != 2 or not isinstance(item[1], int):
                raise ValueError("Invalid reference encoding")
            ref_idx = item[1]
            if ref_idx < 0 or ref_idx >= len(decoded_objects):
                raise ValueError(f"Invalid reference index: {ref_idx}")
            return decoded_objects[ref_idx]
        else:
            raise ValueError(f"Unknown type code: {type_code}")
    
    # First pass: create all objects with placeholders
    for obj_data in objects_data:
        if not isinstance(obj_data, list) or len(obj_data) < 1:
            raise ValueError("Invalid object data in objects list")
        
        type_code = obj_data[0]
        if type_code == 5:  # list
            # Create empty list as placeholder
            decoded_objects.append([])
        elif type_code == 6:  # dict
            # Create empty dict as placeholder
            decoded_objects.append({})
        else:
            raise ValueError(f"Unexpected type code in objects list: {type_code}")
    
    # Second pass: fill in the objects
    for i, obj_data in enumerate(objects_data):
        type_code = obj_data[0]
        if type_code == 5:  # list
            if len(obj_data) != 2 or not isinstance(obj_data[1], list):
                raise ValueError("Invalid list encoding in objects list")
            
            lst = decoded_objects[i]
            lst.clear()  # Clear placeholder
            for encoded_item in obj_data[1]:
                lst.append(_decode_item(encoded_item))
                
        elif type_code == 6:  # dict
            if len(obj_data) != 2 or not isinstance(obj_data[1], list):
                raise ValueError("Invalid dict encoding in objects list")
            
            dct = decoded_objects[i]
            dct.clear()  # Clear placeholder
            for pair in obj_data[1]:
                if not isinstance(pair, list) or len(pair) != 2:
                    raise ValueError("Invalid dict pair encoding")
                key, encoded_value = pair
                if not isinstance(key, str):
                    raise ValueError("Dict key must be str")
                dct[key] = _decode_item(encoded_value)
    
    # Return the root object
    if root_idx < 0 or root_idx >= len(decoded_objects):
        raise ValueError(f"Invalid root index: {root_idx}")
    return decoded_objects[root_idx]