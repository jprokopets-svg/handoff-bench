import json

def encode(obj: object) -> str:
    """Serialize object graph to a string preserving sharing and cycles."""
    obj_to_id = {}  # mapping from python id to assigned index
    serialized = []  # list of serialized complex objects (list/dict)
    
    def _serialize(obj):
        # primitive types
        if isinstance(obj, (int, float, bool, type(None), str)):
            return {"type": "primitive", "value": obj}
        # complex types: list, dict
        if not isinstance(obj, (list, dict)):
            raise ValueError(f"Unsupported type: {type(obj)}")
        
        obj_id = id(obj)
        if obj_id in obj_to_id:
            # already assigned an index
            return {"type": "ref", "id": obj_to_id[obj_id]}
        
        # assign new index
        idx = len(serialized)
        obj_to_id[obj_id] = idx
        # placeholder
        serialized.append(None)
        
        if isinstance(obj, list):
            items = [_serialize(item) for item in obj]
            rep = {"type": "list", "items": items}
        else:  # dict
            # keys must be strings (already guaranteed by problem)
            items = {key: _serialize(value) for key, value in obj.items()}
            rep = {"type": "dict", "items": items}
        
        serialized[idx] = rep
        return {"type": "ref", "id": idx}
    
    root = _serialize(obj)
    # pack everything
    data = {"objects": serialized, "root": root}
    return json.dumps(data)


def decode(s: str) -> object:
    """Deserialize string back to object graph, preserving sharing and cycles."""
    try:
        data = json.loads(s)
    except json.JSONDecodeError:
        raise ValueError("Malformed input")
    
    objects = data["objects"]
    root = data["root"]
    
    # mapping from index to reconstructed object (for complex types)
    decoded = [None] * len(objects)
    
    # first pass: create empty containers
    for i, obj in enumerate(objects):
        if obj["type"] == "list":
            decoded[i] = []
        elif obj["type"] == "dict":
            decoded[i] = {}
        # other types (should not appear)
    
    # second pass: fill containers
    for i, obj in enumerate(objects):
        if obj["type"] == "list":
            target = decoded[i]
            for item in obj["items"]:
                if item["type"] == "ref":
                    target.append(decoded[item["id"]])
                else:
                    target.append(item["value"])
        elif obj["type"] == "dict":
            target = decoded[i]
            for key, item in obj["items"].items():
                if item["type"] == "ref":
                    target[key] = decoded[item["id"]]
                else:
                    target[key] = item["value"]
        # ignore other types
    
    # resolve root
    if root["type"] == "primitive":
        return root["value"]
    else:  # ref
        return decoded[root["id"]]