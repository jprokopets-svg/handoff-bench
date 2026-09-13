import json
from typing import Any, Dict, List


def encode(obj: object) -> str:
    # Assign a unique index to each Python object by its id()
    # Build node entries describing type and references by index
    seen = {}  # id(obj) -> index
    nodes = []

    def add(o):
        oid = id(o)
        if oid in seen:
            return seen[oid]
        idx = len(nodes)
        seen[oid] = idx
        # placeholder to reserve index
        nodes.append(None)

        # Determine type and representation
        if o is None:
            nodes[idx] = {"t": "none"}
        elif isinstance(o, bool):
            # bool is a subclass of int, check before int
            nodes[idx] = {"t": "bool", "v": o}
        elif isinstance(o, int):
            nodes[idx] = {"t": "int", "v": o}
        elif isinstance(o, float):
            nodes[idx] = {"t": "float", "v": o}
        elif isinstance(o, str):
            nodes[idx] = {"t": "str", "v": o}
        elif isinstance(o, list):
            # recursively add children
            children = []
            for item in o:
                children.append(add(item))
            nodes[idx] = {"t": "list", "v": children}
        elif isinstance(o, dict):
            # only allow string keys
            mapping = {}
            for k, v in o.items():
                if not isinstance(k, str):
                    raise ValueError("Only string dict keys are supported")
                mapping[k] = add(v)
            nodes[idx] = {"t": "dict", "v": mapping}
        else:
            raise ValueError(f"Unsupported type: {type(o)!r}")
        return idx

    root_idx = add(obj)
    out = {"root": root_idx, "nodes": nodes}
    try:
        return json.dumps(out, separators=(",", ":"), ensure_ascii=False)
    except (TypeError, ValueError):
        # propagate as ValueError
        raise


def decode(s: str) -> object:
    try:
        data = json.loads(s)
    except Exception as e:
        raise ValueError("Malformed input: not valid JSON") from e

    if not isinstance(data, dict):
        raise ValueError("Malformed input: top-level must be an object")
    if "root" not in data or "nodes" not in data:
        raise ValueError("Malformed input: missing root or nodes")
    root = data["root"]
    nodes = data["nodes"]
    if not isinstance(root, int):
        raise ValueError("Malformed input: root must be int")
    if not isinstance(nodes, list):
        raise ValueError("Malformed input: nodes must be list")

    # First pass: create placeholders or primitive values
    n = len(nodes)
    if not (0 <= root < n):
        raise ValueError("Malformed input: root index out of range")

    objects: List[Any] = [None] * n

    for i, node in enumerate(nodes):
        if not isinstance(node, dict):
            raise ValueError("Malformed input: each node must be object")
        if "t" not in node:
            raise ValueError("Malformed input: node missing type")
        t = node["t"]
        if t == "none":
            objects[i] = None
        elif t == "bool":
            if "v" not in node or not isinstance(node["v"], bool):
                raise ValueError("Malformed input: invalid bool node")
            objects[i] = node["v"]
        elif t == "int":
            if "v" not in node or not isinstance(node["v"], int):
                # JSON may parse numbers as int or float; require int
                raise ValueError("Malformed input: invalid int node")
            objects[i] = node["v"]
        elif t == "float":
            if "v" not in node or not (isinstance(node["v"], float) or isinstance(node["v"], int)):
                # JSON may give ints for floats; accept int too and convert
                raise ValueError("Malformed input: invalid float node")
            objects[i] = float(node["v"])
        elif t == "str":
            if "v" not in node or not isinstance(node["v"], str):
                raise ValueError("Malformed input: invalid str node")
            objects[i] = node["v"]
        elif t == "list":
            if "v" not in node or not isinstance(node["v"], list):
                raise ValueError("Malformed input: invalid list node")
            # placeholder list to be filled later
            objects[i] = []
        elif t == "dict":
            if "v" not in node or not isinstance(node["v"], dict):
                raise ValueError("Malformed input: invalid dict node")
            # keys must be strings and values indices
            objects[i] = {}
        else:
            raise ValueError("Malformed input: unknown node type")

    # Second pass: fill containers
    for i, node in enumerate(nodes):
        t = node["t"]
        if t == "list":
            children = node["v"]
            lst = objects[i]
            for idx in children:
                if not isinstance(idx, int) or not (0 <= idx < n):
                    raise ValueError("Malformed input: invalid child index")
                lst.append(objects[idx])
        elif t == "dict":
            mapping = node["v"]
            d = objects[i]
            for k, idx in mapping.items():
                if not isinstance(k, str):
                    raise ValueError("Malformed input: dict keys must be strings")
                if not isinstance(idx, int) or not (0 <= idx < n):
                    raise ValueError("Malformed input: invalid dict child index")
                d[k] = objects[idx]

    return objects[root]
