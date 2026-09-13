import json
from typing import Any, Dict, List, Union

def encode(obj: object) -> str:
    """Serialize object graph to a string preserving sharing and cycles."""
    # Mapping from object id to assigned index
    obj_to_id: Dict[int, int] = {}
    # List of encoded objects
    encoded_objects: List[Any] = []
    
    def _encode(obj: Any) -> int:
        """Encode object, return its index."""
        # For primitive immutable types, we can encode directly without storing id
        # But we need to handle sharing: same primitive value should be same object?
        # In Python, small ints and some strings are interned, but not guaranteed.
        # The spec says "same object appears multiple times" - for immutable primitives,
        # identity may not be preserved after decode anyway (e.g., two separate int 5).
        # However, test expects out[0] is out[1] for list sharing.
        # For immutable primitives, we can treat them as values, not references.
        # But sharing of same int object? In Python, ints are immutable; two references
        # to same int value may be same object due to interning, but not required.
        # We'll encode primitives as values, not track identity.
        # However, for list/dict we need identity.
        
        # Check type
        if isinstance(obj, int):
            # type 0
            encoded = [0, obj]
        elif isinstance(obj, float):
            encoded = [1, obj]
        elif isinstance(obj, bool):
            encoded = [2, obj]
        elif obj is None:
            encoded = [3, None]
        elif isinstance(obj, str):
            encoded = [4, obj]
        elif isinstance(obj, list):
            # Check if already visited
            obj_id = id(obj)
            if obj_id in obj_to_id:
                return obj_to_id[obj_id]
            # Assign new id
            idx = len(encoded_objects)
            obj_to_id[obj_id] = idx
            # Placeholder entry, will be filled later
            encoded_objects.append(None)
            # Encode children
            child_indices = [_encode(item) for item in obj]
            encoded = [5, child_indices]
            # Update placeholder
            encoded_objects[idx] = encoded
            return idx
        elif isinstance(obj, dict):
            # keys must be strings
            for key in obj.keys():
                if not isinstance(key, str):
                    raise ValueError("Dict keys must be strings")
            obj_id = id(obj)
            if obj_id in obj_to_id:
                return obj_to_id[obj_id]
            idx = len(encoded_objects)
            obj_to_id[obj_id] = idx
            encoded_objects.append(None)
            # Encode as list of pairs (key, value_index)
            items = []
            for k, v in obj.items():
                items.append([k, _encode(v)])
            encoded = [6, items]
            encoded_objects[idx] = encoded
            return idx
        else:
            raise ValueError(f"Unsupported type: {type(obj)}")
        
        # For primitive types, we don't need to store identity; just encode directly.
        # However, we still need to assign an index for consistency? Actually we can
        # encode primitives inline in the object list, but they don't need reference tracking.
        # We'll just add to encoded_objects and return index.
        idx = len(encoded_objects)
        encoded_objects.append(encoded)
        return idx
    
    root_idx = _encode(obj)
    # Build final structure: [root_index, encoded_objects]
    result = [root_idx, encoded_objects]
    return json.dumps(result, ensure_ascii=False)


def decode(s: str) -> object:
    """Deserialize string back to object graph preserving sharing and cycles."""
    try:
        data = json.loads(s)
    except json.JSONDecodeError:
        raise ValueError("Malformed JSON")
    
    if not isinstance(data, list) or len(data) != 2:
        raise ValueError("Invalid format")
    root_idx, encoded_objects = data
    if not isinstance(root_idx, int) or not isinstance(encoded_objects, list):
        raise ValueError("Invalid format")
    
    # Mapping from index to decoded object (for lists/dicts)
    decoded: Dict[int, Any] = {}
    
    def _decode(idx: int) -> Any:
        """Decode object at given index."""
        # If already decoded (for lists/dicts), return
        if idx in decoded:
            return decoded[idx]
        
        enc = encoded_objects[idx]
        if not isinstance(enc, list) or len(enc) < 1:
            raise ValueError("Invalid encoded object")
        typ = enc[0]
        if not isinstance(typ, int):
            raise ValueError("Invalid type")
        
        if typ == 0:  # int
            val = enc[1]
            if not isinstance(val, int):
                raise ValueError("Invalid int")
            return val
        elif typ == 1:  # float
            val = enc[1]
            if not isinstance(val, (int, float)):
                raise ValueError("Invalid float")
            return float(val)
        elif typ == 2:  # bool
            val = enc[1]
            if not isinstance(val, bool):
                raise ValueError("Invalid bool")
            return val
        elif typ == 3:  # None
            if enc[1] is not None:
                raise ValueError("Invalid None")
            return None
        elif typ == 4:  # str
            val = enc[1]
            if not isinstance(val, str):
                raise ValueError("Invalid str")
            return val
        elif typ == 5:  # list
            # list of child indices
            child_indices = enc[1]
            if not isinstance(child_indices, list):
                raise ValueError("Invalid list encoding")
            # Create empty list and store in decoded map before decoding children
            # to handle cycles
            lst = []
            decoded[idx] = lst
            # Decode children
            for child_idx in child_indices:
                if not isinstance(child_idx, int):
                    raise ValueError("Invalid child index")
                lst.append(_decode(child_idx))
            return lst
        elif typ == 6:  # dict
            items = enc[1]
            if not isinstance(items, list):
                raise ValueError("Invalid dict encoding")
            d = {}
            decoded[idx] = d
            for item in items:
                if not isinstance(item, list) or len(item) != 2:
                    raise ValueError("Invalid dict item")
                key, val_idx = item
                if not isinstance(key, str):
                    raise ValueError("Dict key must be string")
                if not isinstance(val_idx, int):
                    raise ValueError("Invalid value index")
                d[key] = _decode(val_idx)
            return d
        else:
            raise ValueError(f"Unknown type code {typ}")
    
    return _decode(root_idx)