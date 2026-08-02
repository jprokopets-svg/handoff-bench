import json
from typing import Any, Dict


def encode(obj: object) -> str:
    """Serialize object graph preserving shared references and cycles.
    Supported types: int, float, bool, None, str, list, dict (string keys).
    """
    # Use id(obj) to track identity
    next_id = 0
    id_map: Dict[int, int] = {}  # mapping from id(obj) -> node id
    obj_map: Dict[int, object] = {}  # mapping from id(obj) -> object
    nodes = []
    queue = [obj]

    while queue:
        cur = queue.pop(0)
        cur_key = id(cur)
        if cur_key in id_map:
            continue
        # Assign id
        nid = next_id
        next_id += 1
        id_map[cur_key] = nid
        obj_map[cur_key] = cur

        # Determine type
        if cur is None:
            ntype = "null"
            nvalue = None
        elif isinstance(cur, bool):
            ntype = "bool"
            nvalue = cur
        elif isinstance(cur, int):
            ntype = "int"
            nvalue = cur
        elif isinstance(cur, float):
            ntype = "float"
            nvalue = cur
        elif isinstance(cur, str):
            ntype = "str"
            nvalue = cur
        elif isinstance(cur, list):
            ntype = "list"
            # For lists store child ids (assign ids lazily)
            child_ids = []
            for item in cur:
                if not (isinstance(item, (int, float, bool, str, list, dict)) or item is None):
                    raise ValueError(f"Unsupported type in list: {type(item)}")
                queue.append(item)
                # child id may not yet be assigned; we will set placeholder using id(item)
                child_ids.append(id(item))
            nvalue = child_ids
        elif isinstance(cur, dict):
            ntype = "dict"
            d = {}
            for k, v in cur.items():
                if not isinstance(k, str):
                    raise ValueError("Dict keys must be strings")
                if not (isinstance(v, (int, float, bool, str, list, dict)) or v is None):
                    raise ValueError(f"Unsupported type in dict: {type(v)}")
                queue.append(v)
                d[k] = id(v)
            nvalue = d
        else:
            raise ValueError(f"Unsupported type: {type(cur)}")

        nodes.append({"id": nid, "type": ntype, "value": nvalue})

    # Now nodes contain entries with value referencing children by Python id. We need to replace those with node ids.
    # Build reverse map from obj id -> assigned node id
    reverse = id_map  # name alias

    # Convert node values
    out_nodes = []
    # Sort nodes by their assigned node id to ensure deterministic output
    nodes.sort(key=lambda n: n["id"])
    for node in nodes:
        ntype = node["type"]
        nvalue = node["value"]
        nid = node["id"]
        if ntype == "list":
            # nvalue is list of object ids
            child_node_ids = []
            for objid in nvalue:
                if objid not in reverse:
                    # This should not happen
                    raise ValueError("Internal encoding error: unknown child")
                child_node_ids.append(reverse[objid])
            out_nodes.append({"id": nid, "type": "list", "value": child_node_ids})
        elif ntype == "dict":
            d = {}
            for k, objid in nvalue.items():
                if objid not in reverse:
                    raise ValueError("Internal encoding error: unknown child")
                d[k] = reverse[objid]
            out_nodes.append({"id": nid, "type": "dict", "value": d})
        else:
            # primitives
            out_nodes.append({"id": nid, "type": ntype, "value": nvalue})

    payload = {"nodes": out_nodes, "root": id_map[id(obj)]}
    return json.dumps(payload, ensure_ascii=False)


def decode(s: str) -> object:
    """Decode string produced by encode back into object graph preserving identity and cycles."""
    try:
        payload = json.loads(s)
    except Exception as e:
        raise ValueError("Malformed input: not valid JSON") from e

    if not isinstance(payload, dict):
        raise ValueError("Malformed input: expected object")
    if "nodes" not in payload or "root" not in payload:
        raise ValueError("Malformed input: missing keys")
    nodes = payload["nodes"]
    root = payload["root"]
    if not isinstance(nodes, list):
        raise ValueError("Malformed input: nodes must be a list")
    # Build id->node map
    node_map: Dict[int, Dict[str, Any]] = {}
    for entry in nodes:
        if not isinstance(entry, dict):
            raise ValueError("Malformed input: node entry must be object")
        if "id" not in entry or "type" not in entry or "value" not in entry:
            raise ValueError("Malformed input: node missing fields")
        nid = entry["id"]
        if not isinstance(nid, int):
            raise ValueError("Malformed input: node id must be int")
        if nid in node_map:
            raise ValueError("Malformed input: duplicate node id")
        node_map[nid] = entry

    if not isinstance(root, int) or root not in node_map:
        raise ValueError("Malformed input: invalid root id")

    # Create placeholders
    placeholders: Dict[int, object] = {}
    for nid, entry in node_map.items():
        ntype = entry["type"]
        value = entry["value"]
        if ntype == "null":
            placeholders[nid] = None
        elif ntype == "bool":
            if not isinstance(value, bool):
                raise ValueError("Malformed input: bool node value not bool")
            placeholders[nid] = value
        elif ntype == "int":
            if not isinstance(value, int) or isinstance(value, bool):
                # bools are instances of int in JSON -> but JSON true/false map to bool, so this protects
                raise ValueError("Malformed input: int node value not int")
            placeholders[nid] = value
        elif ntype == "float":
            if not (isinstance(value, float) or isinstance(value, int)):
                # JSON may represent floats as ints if whole number
                raise ValueError("Malformed input: float node value not float")
            placeholders[nid] = float(value)
        elif ntype == "str":
            if not isinstance(value, str):
                raise ValueError("Malformed input: str node value not string")
            placeholders[nid] = value
        elif ntype == "list":
            if not isinstance(value, list):
                raise ValueError("Malformed input: list node value not list")
            placeholders[nid] = []
        elif ntype == "dict":
            if not isinstance(value, dict):
                raise ValueError("Malformed input: dict node value not object")
            # Ensure keys are strings
            for k in value.keys():
                if not isinstance(k, str):
                    raise ValueError("Malformed input: dict node has non-string key")
            placeholders[nid] = {}
        else:
            raise ValueError("Malformed input: unknown node type")

    # Second pass: fill composite nodes
    for nid, entry in node_map.items():
        ntype = entry["type"]
        value = entry["value"]
        if ntype == "list":
            # value is list of node ids
            lst = placeholders[nid]
            assert isinstance(lst, list)
            for cid in value:
                if not isinstance(cid, int) or cid not in placeholders:
                    raise ValueError("Malformed input: invalid child id in list")
                lst.append(placeholders[cid])
        elif ntype == "dict":
            dct = placeholders[nid]
            assert isinstance(dct, dict)
            for k, cid in value.items():
                if not isinstance(cid, int) or cid not in placeholders:
                    raise ValueError("Malformed input: invalid child id in dict")
                dct[k] = placeholders[cid]
        # primitives already set

    return placeholders[root]
