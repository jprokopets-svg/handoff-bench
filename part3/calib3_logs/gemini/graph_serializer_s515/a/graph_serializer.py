
import json

def encode(obj):
    """
    Serializes a Python object graph to a JSON string, preserving shared
    references and cycles.
    """
    memo = {}
    objects = []

    def _encode(o):
        if id(o) in memo:
            return {"$ref": memo[id(o)]}

        if isinstance(o, (list, dict)):
            obj_id = len(objects)
            memo[id(o)] = obj_id
            if isinstance(o, list):
                placeholder = {"$type": "list", "id": obj_id, "value": []}
                objects.append(placeholder)
                placeholder["value"] = [_encode(item) for item in o]
            else: # dict
                if not all(isinstance(k, str) for k in o.keys()):
                    raise ValueError("Dictionary keys must be strings")
                placeholder = {"$type": "dict", "id": obj_id, "value": {}}
                objects.append(placeholder)
                placeholder["value"] = {k: _encode(v) for k, v in o.items()}
            return {"$ref": obj_id}
        elif isinstance(o, (int, float, bool, type(None), str)):
            return o
        else:
            raise ValueError(f"Unsupported type: {type(o)}")

    root = _encode(obj)
    return json.dumps({"root": root, "objects": objects})

def decode(s):
    """
    Deserializes a JSON string created by encode() back into a Python
    object graph.
    """
    try:
        data = json.loads(s)
        if not isinstance(data, dict) or "root" not in data or "objects" not in data:
            raise ValueError("Invalid format")
    except (json.JSONDecodeError, TypeError):
        raise ValueError("Malformed JSON")


    objects = data["objects"]
    memo = {}

    # First pass: create empty containers
    for obj_def in objects:
        if not isinstance(obj_def, dict) or "$type" not in obj_def or "id" not in obj_def:
            raise ValueError("Invalid object definition")
        obj_id = obj_def["id"]
        if obj_def["$type"] == "list":
            memo[obj_id] = []
        elif obj_def["$type"] == "dict":
            memo[obj_id] = {}
        else:
            raise ValueError(f"Unknown object type: {obj_def['$type']}")

    # Second pass: populate containers
    for obj_def in objects:
        obj_id = obj_def["id"]
        container = memo[obj_id]
        value = obj_def["value"]

        if obj_def["$type"] == "list":
            for item in value:
                container.append(_decode_value(item, memo))
        elif obj_def["$type"] == "dict":
            for k, v in value.items():
                container[k] = _decode_value(v, memo)

    return _decode_value(data["root"], memo)

def _decode_value(v, memo):
    if isinstance(v, dict) and "$ref" in v:
        try:
            return memo[v["$ref"]]
        except (KeyError, TypeError):
            raise ValueError(f"Invalid reference: {v['$ref']}")
    return v
