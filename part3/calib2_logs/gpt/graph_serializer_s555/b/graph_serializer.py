import json
from typing import Any


def encode(obj: object) -> str:
    """Serialize object graph to a JSON string preserving shared references and cycles.

    Format:
    {
      "root": uid_str,
      "nodes": { uid_str: {"t": type_tag, "v": value_or_refs } }
    }

    type_tag: one of "int","float","bool","null","str","list","dict"
    For list: v is list of uid_str
    For dict: v is mapping from string key to uid_str
    For primitives: v is the primitive value (JSON-serializable)
    """
    obj_to_uid = {}
    nodes = {}
    next_uid = 0

    def new_uid():
        nonlocal next_uid
        uid = str(next_uid)
        next_uid += 1
        return uid

    def add(o: Any) -> str:
        oid = id(o)
        if oid in obj_to_uid:
            return obj_to_uid[oid]
        # assign uid early to allow cycles
        uid = new_uid()
        obj_to_uid[oid] = uid

        # Determine type
        if o is None:
            nodes[uid] = {"t": "null", "v": None}
        elif isinstance(o, bool):
            # bool is subclass of int so check before int
            nodes[uid] = {"t": "bool", "v": o}
        elif isinstance(o, int):
            nodes[uid] = {"t": "int", "v": o}
        elif isinstance(o, float):
            nodes[uid] = {"t": "float", "v": o}
        elif isinstance(o, str):
            nodes[uid] = {"t": "str", "v": o}
        elif isinstance(o, list):
            # placeholder list to allow cycles
            nodes[uid] = {"t": "list", "v": []}
            # fill with references
            vals = []
            for item in o:
                if not _is_supported(item):
                    raise ValueError(f"Unsupported type: {type(item)!r}")
                vals.append(add(item))
            nodes[uid]["v"] = vals
        elif isinstance(o, dict):
            # keys must be strings
            for k in o.keys():
                if not isinstance(k, str):
                    raise ValueError("Dict keys must be strings")
            nodes[uid] = {"t": "dict", "v": {}}
            mapping = {}
            for k, v in o.items():
                if not _is_supported(v):
                    raise ValueError(f"Unsupported type: {type(v)!r}")
                mapping[k] = add(v)
            nodes[uid]["v"] = mapping
        else:
            raise ValueError(f"Unsupported type: {type(o)!r}")
        return uid

    def _is_supported(x: Any) -> bool:
        return (x is None or isinstance(x, (bool, int, float, str, list, dict)))

    root_uid = add(obj)
    out = {"root": root_uid, "nodes": nodes}
    return json.dumps(out, separators=(",", ":"), ensure_ascii=False)


def decode(s: str) -> object:
    """Decode string produced by encode back into Python objects, preserving shared refs/cycles.

    Raises ValueError on malformed input.
    """
    try:
        data = json.loads(s)
    except Exception as e:
        raise ValueError("Malformed input: not valid JSON") from e

    if not isinstance(data, dict):
        raise ValueError("Malformed input: top-level must be object")
    if "root" not in data or "nodes" not in data:
        raise ValueError("Malformed input: missing root or nodes")
    nodes = data["nodes"]
    root = data["root"]
    if not isinstance(nodes, dict):
        raise ValueError("Malformed input: nodes must be object")
    if root not in nodes:
        raise ValueError("Malformed input: root not in nodes")

    # First pass: validate structure and create placeholders
    placeholders = {}
    types = {}

    for uid, node in nodes.items():
        if not isinstance(uid, str):
            raise ValueError("Malformed input: node uid must be string")
        if not isinstance(node, dict):
            raise ValueError("Malformed input: node must be object")
        if "t" not in node or "v" not in node:
            raise ValueError("Malformed input: node missing t or v")
        t = node["t"]
        v = node["v"]
        types[uid] = t
        if t == "null":
            placeholders[uid] = None
        elif t == "bool":
            if not isinstance(v, bool):
                raise ValueError("Malformed input: bool node v must be boolean")
            placeholders[uid] = v
        elif t == "int":
            if not isinstance(v, int):
                raise ValueError("Malformed input: int node v must be integer")
            placeholders[uid] = v
        elif t == "float":
            if not (isinstance(v, float) or isinstance(v, int)):
                raise ValueError("Malformed input: float node v must be number")
            placeholders[uid] = float(v)
        elif t == "str":
            if not isinstance(v, str):
                raise ValueError("Malformed input: str node v must be string")
            placeholders[uid] = v
        elif t == "list":
            if not isinstance(v, list):
                raise ValueError("Malformed input: list node v must be array")
            # create empty list placeholder
            placeholders[uid] = []
        elif t == "dict":
            if not isinstance(v, dict):
                raise ValueError("Malformed input: dict node v must be object")
            # keys must be strings (json ensures), create empty dict placeholder
            placeholders[uid] = {}
        else:
            raise ValueError("Malformed input: unknown node type")

    # Second pass: fill containers resolving references
    for uid, node in nodes.items():
        t = node["t"]
        v = node["v"]
        if t == "list":
            lst = placeholders[uid]
            # v should be list of uids (strings)
            for ref in v:
                if not isinstance(ref, str) or ref not in placeholders:
                    raise ValueError("Malformed input: invalid reference in list")
                lst.append(placeholders[ref])
        elif t == "dict":
            dct = placeholders[uid]
            for k, ref in v.items():
                if not isinstance(k, str):
                    raise ValueError("Malformed input: dict key must be string")
                if not isinstance(ref, str) or ref not in placeholders:
                    raise ValueError("Malformed input: invalid reference in dict")
                dct[k] = placeholders[ref]
        # primitives already set

    return placeholders[root]
