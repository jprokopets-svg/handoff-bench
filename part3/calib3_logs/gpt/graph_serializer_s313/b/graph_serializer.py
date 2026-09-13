import json
from typing import Any


def encode(obj: object) -> str:
    """Encode a Python object graph to a JSON string preserving shared references and cycles.

    Supported types: int, float, bool, None, str, list, dict (with string keys).
    """
    # Helper to check primitive supported types
    def is_primitive(o):
        return o is None or isinstance(o, (bool, int, float, str))

    # Containers we will assign ids to
    if is_primitive(obj):
        # Even if primitive, we can encode directly with empty nodes
        root = obj
        nodes = {}
        return json.dumps({"root": root, "nodes": nodes}, ensure_ascii=False)

    # Only list and dict supported as top-level non-primitive containers
    if not isinstance(obj, (list, dict)):
        raise ValueError(f"Unsupported type: {type(obj)}")

    id_map = {}  # id(obj) -> node_id
    nodes = {}  # node_id -> {"t": "list"/"dict", "v": ...}
    next_idx = 1

    def new_id():
        nonlocal next_idx
        nid = f"n{next_idx}"
        next_idx += 1
        return nid

    # assign id to root
    def assign(obj):
        oid = id(obj)
        if oid in id_map:
            return id_map[oid]
        nid = new_id()
        id_map[oid] = nid
        # create placeholder in nodes
        if isinstance(obj, list):
            nodes[nid] = {"t": "list", "v": None}
        else:
            nodes[nid] = {"t": "dict", "v": None}
        stack.append(obj)
        return nid

    stack = []
    root_id = assign(obj)

    # process stack
    while stack:
        current = stack.pop()
        cid = id_map[id(current)]
        if isinstance(current, list):
            out_list = []
            for item in current:
                if is_primitive(item):
                    out_list.append(item)
                elif isinstance(item, (list, dict)):
                    child_id = assign(item)
                    out_list.append({"$ref": child_id})
                else:
                    raise ValueError(f"Unsupported type in list: {type(item)}")
            nodes[cid]["v"] = out_list
        else:  # dict
            out_dict = {}
            for k, v in current.items():
                if not isinstance(k, str):
                    raise ValueError("Dict keys must be strings")
                if is_primitive(v):
                    out_dict[k] = v
                elif isinstance(v, (list, dict)):
                    child_id = assign(v)
                    out_dict[k] = {"$ref": child_id}
                else:
                    raise ValueError(f"Unsupported type in dict: {type(v)}")
            nodes[cid]["v"] = out_dict

    # root should be a ref to the root container
    root_rep = {"$ref": root_id}
    return json.dumps({"root": root_rep, "nodes": nodes}, ensure_ascii=False)


def decode(s: str) -> object:
    """Decode a string produced by encode back into the Python object graph.

    Raises ValueError on malformed input.
    """
    try:
        data = json.loads(s)
    except Exception as e:
        raise ValueError("Invalid JSON") from e

    if not isinstance(data, dict):
        raise ValueError("Top-level must be an object")
    if "root" not in data or "nodes" not in data:
        raise ValueError("Missing 'root' or 'nodes'")
    nodes = data["nodes"]
    root = data["root"]
    if not isinstance(nodes, dict):
        raise ValueError("'nodes' must be an object")

    # Validate node ids are strings
    for nid in nodes.keys():
        if not isinstance(nid, str):
            raise ValueError("Node ids must be strings")

    # First pass: create placeholders
    placeholders = {}
    for nid, node in nodes.items():
        if not isinstance(node, dict):
            raise ValueError("Each node must be an object")
        if "t" not in node or "v" not in node:
            raise ValueError("Node missing 't' or 'v'")
        t = node["t"]
        if t == "list":
            placeholders[nid] = []
        elif t == "dict":
            placeholders[nid] = {}
        else:
            raise ValueError("Unknown node type")

    # Helper to resolve a value
    def resolve(val):
        # A ref must be a dict with single key "$ref"
        if isinstance(val, dict) and set(val.keys()) == {"$ref"}:
            ref = val["$ref"]
            if not isinstance(ref, str):
                raise ValueError("$ref must be a string id")
            if ref not in placeholders:
                raise ValueError("Unknown $ref id")
            return placeholders[ref]
        # otherwise primitive
        if val is None or isinstance(val, (bool, int, float, str)):
            return val
        raise ValueError("Invalid value in node")

    # Second pass: fill placeholders
    for nid, node in nodes.items():
        t = node["t"]
        v = node["v"]
        if t == "list":
            if not isinstance(v, list):
                raise ValueError("List node 'v' must be a list")
            lst = placeholders[nid]
            for item in v:
                lst.append(resolve(item))
        else:  # dict
            if not isinstance(v, dict):
                raise ValueError("Dict node 'v' must be an object")
            dct = placeholders[nid]
            for k, val in v.items():
                if not isinstance(k, str):
                    raise ValueError("Dict keys must be strings")
                dct[k] = resolve(val)

    # Resolve root
    if isinstance(root, dict) and set(root.keys()) == {"$ref"}:
        ref = root["$ref"]
        if not isinstance(ref, str) or ref not in placeholders:
            raise ValueError("Invalid root $ref")
        return placeholders[ref]
    # Root can be a primitive
    if root is None or isinstance(root, (bool, int, float, str)):
        return root
    raise ValueError("Invalid root value")
