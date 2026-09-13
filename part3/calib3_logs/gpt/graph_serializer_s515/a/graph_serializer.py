import json


class GraphSerializerError(ValueError):
    pass


def encode(obj):
    """Serialize object graph preserving shared refs and cycles."""
    # Supported types: int, float, bool, None, str, list, dict with string keys
    # We'll assign an index to each distinct Python object (by id) encountered
    # and output a JSON dict with nodes and root index.

    next_index = 0
    obj_to_index = {}
    nodes = []  # list of node dicts

    def add_obj(o):
        nonlocal next_index
        oid = id(o)
        if oid in obj_to_index:
            return obj_to_index[oid]
        idx = next_index
        next_index += 1
        obj_to_index[oid] = idx
        nodes.append(None)  # placeholder
        # We'll fill nodes[idx] with proper representation depending on type
        if isinstance(o, bool):
            nodes[idx] = {"t": "bool", "v": o}
        elif o is None:
            nodes[idx] = {"t": "none", "v": None}
        elif isinstance(o, int):
            nodes[idx] = {"t": "int", "v": o}
        elif isinstance(o, float):
            nodes[idx] = {"t": "float", "v": o}
        elif isinstance(o, str):
            nodes[idx] = {"t": "str", "v": o}
        elif isinstance(o, list):
            # For containers, temporarily set empty list of refs, then traverse children
            nodes[idx] = {"t": "list", "v": []}
            # We must traverse children and add refs
            for item in o:
                # allowed types check deferred to recursive add
                child_idx = add_obj(item)
                nodes[idx]["v"].append(child_idx)
        elif isinstance(o, dict):
            # keys must be strings
            for k in o.keys():
                if not isinstance(k, str):
                    raise ValueError("Only string keys supported in dict")
            nodes[idx] = {"t": "dict", "v": []}
            for k, v in o.items():
                child_idx = add_obj(v)
                nodes[idx]["v"].append([k, child_idx])
        else:
            raise ValueError(f"Unsupported type: {type(o)!r}")
        return idx

    root_idx = add_obj(obj)
    out = {"nodes": nodes, "root": root_idx}
    try:
        return json.dumps(out, ensure_ascii=False)
    except Exception as e:
        raise


def decode(s):
    """Decode string produced by encode back into object graph with identity preserved."""
    try:
        data = json.loads(s)
    except Exception:
        raise ValueError("Malformed input")
    if not isinstance(data, dict) or "nodes" not in data or "root" not in data:
        raise ValueError("Malformed input")
    nodes = data["nodes"]
    root = data["root"]
    if not isinstance(nodes, list) or not isinstance(root, int):
        raise ValueError("Malformed input")
    n = len(nodes)
    # Validate nodes entries basic shape
    for i, node in enumerate(nodes):
        if not isinstance(node, dict) or "t" not in node or "v" not in node:
            raise ValueError("Malformed input")
        if not isinstance(node["t"], str):
            raise ValueError("Malformed input")

    # First pass: create placeholders / primitive objects
    objs = [None] * n
    for i, node in enumerate(nodes):
        t = node["t"]
        v = node["v"]
        if t == "list":
            if not isinstance(v, list):
                raise ValueError("Malformed input")
            objs[i] = []
        elif t == "dict":
            if not isinstance(v, list):
                raise ValueError("Malformed input")
            objs[i] = {}
        elif t == "int":
            if not isinstance(v, int) or isinstance(v, bool):
                # bool is subclass of int so ensure not bool
                raise ValueError("Malformed input")
            objs[i] = v
        elif t == "float":
            if not isinstance(v, (int, float)):
                # JSON may decode floats as int if integer-valued; accept both
                raise ValueError("Malformed input")
            objs[i] = float(v)
        elif t == "bool":
            if not isinstance(v, bool):
                raise ValueError("Malformed input")
            objs[i] = v
        elif t == "none":
            if v is not None:
                raise ValueError("Malformed input")
            objs[i] = None
        elif t == "str":
            if not isinstance(v, str):
                raise ValueError("Malformed input")
            objs[i] = v
        else:
            raise ValueError("Malformed input")

    # Second pass: fill containers
    for i, node in enumerate(nodes):
        t = node["t"]
        v = node["v"]
        if t == "list":
            lst = objs[i]
            # expect v is list of indices
            for ref in v:
                if not isinstance(ref, int) or not (0 <= ref < n):
                    raise ValueError("Malformed input")
                lst.append(objs[ref])
        elif t == "dict":
            d = objs[i]
            for pair in v:
                if not (isinstance(pair, list) or isinstance(pair, tuple)) or len(pair) != 2:
                    raise ValueError("Malformed input")
                key, ref = pair
                if not isinstance(key, str):
                    raise ValueError("Malformed input")
                if not isinstance(ref, int) or not (0 <= ref < n):
                    raise ValueError("Malformed input")
                d[key] = objs[ref]
        # primitives already set

    if not (0 <= root < n):
        raise ValueError("Malformed input")
    return objs[root]


if __name__ == '__main__':
    # quick manual test
    pass
