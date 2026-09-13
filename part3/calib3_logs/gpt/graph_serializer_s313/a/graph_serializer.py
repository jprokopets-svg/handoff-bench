import json


class GraphSerializerError(ValueError):
    pass


def encode(obj):
    """Serialize supported Python object graph preserving shared references and cycles.
    Returns a JSON string.
    Supported types: int, float, bool, None, str, list, dict(with string keys).
    """
    # nodes: id_str -> {'t': 'list'|'dict', 'v': ...}
    nodes = {}
    seen = {}  # map id(obj) -> id_str for containers
    counter = [0]

    def next_id():
        i = counter[0]
        counter[0] += 1
        return str(i)

    def serialize(o):
        # primitives
        if o is None:
            return None
        if isinstance(o, bool):
            return o
        if isinstance(o, int):
            return o
        if isinstance(o, float):
            return o
        if isinstance(o, str):
            return o
        # containers
        if isinstance(o, list):
            oid = seen.get(id(o))
            if oid is not None:
                return {"$ref": oid}
            oid = next_id()
            seen[id(o)] = oid
            # create placeholder
            nodes[oid] = {"t": "list", "v": None}
            # fill contents
            nodes[oid]["v"] = [serialize(x) for x in o]
            return {"$ref": oid}
        if isinstance(o, dict):
            # keys must be strings
            for k in o.keys():
                if not isinstance(k, str):
                    raise ValueError("Dict keys must be strings")
            oid = seen.get(id(o))
            if oid is not None:
                return {"$ref": oid}
            oid = next_id()
            seen[id(o)] = oid
            nodes[oid] = {"t": "dict", "v": None}
            d = {}
            for k, v in o.items():
                d[k] = serialize(v)
            nodes[oid]["v"] = d
            return {"$ref": oid}
        # unsupported
        raise ValueError(f"Unsupported type: {type(o)!r}")

    root = serialize(obj)
    # final structure
    out = {"root": root, "nodes": nodes}
    return json.dumps(out, ensure_ascii=False)


def decode(s):
    """Decode the string produced by encode back into object graph.
    Raises ValueError for malformed input.
    """
    try:
        data = json.loads(s)
    except Exception as e:
        raise ValueError("Invalid input: not valid JSON") from None

    if not isinstance(data, dict):
        raise ValueError("Malformed input: top-level must be an object")
    if "root" not in data or "nodes" not in data:
        raise ValueError("Malformed input: missing root or nodes")
    nodes_data = data["nodes"]
    root = data["root"]
    if not isinstance(nodes_data, dict):
        raise ValueError("Malformed input: nodes must be an object")

    # create placeholders
    obj_map = {}
    for nid, node in nodes_data.items():
        if not isinstance(nid, str):
            raise ValueError("Malformed input: node ids must be strings")
        if not isinstance(node, dict):
            raise ValueError("Malformed input: node must be an object")
        t = node.get("t")
        v = node.get("v")
        if t == "list":
            if v is None:
                # allow empty list encoded as v == [] normally, but v None is malformed
                pass
            obj_map[nid] = []
        elif t == "dict":
            obj_map[nid] = {}
        else:
            raise ValueError("Malformed input: unknown node type")

    def is_ref(obj):
        return isinstance(obj, dict) and list(obj.keys()) == ["$ref"]

    def deserialize(val):
        # primitives
        if val is None or isinstance(val, (bool, int, float, str)):
            return val
        # reference wrapper
        if is_ref(val):
            rid = val["$ref"]
            if not isinstance(rid, str):
                raise ValueError("Malformed input: $ref must be a string id")
            if rid not in obj_map:
                raise ValueError("Malformed input: reference to unknown id")
            return obj_map[rid]
        # any other dict is malformed
        raise ValueError("Malformed input: unexpected dict value")

    # fill contents
    for nid, node in nodes_data.items():
        t = node.get("t")
        v = node.get("v")
        target = obj_map[nid]
        if t == "list":
            if not isinstance(v, list):
                raise ValueError("Malformed input: list node must have list v")
            # populate list
            target.extend(deserialize(item) for item in v)
        elif t == "dict":
            if not isinstance(v, dict):
                raise ValueError("Malformed input: dict node must have object v")
            for k, val in v.items():
                if not isinstance(k, str):
                    raise ValueError("Malformed input: dict node keys must be strings")
                target[k] = deserialize(val)
        else:
            raise ValueError("Malformed input: unknown node type")

    # finally get root
    if is_ref(root):
        rid = root["$ref"]
        if not isinstance(rid, str) or rid not in obj_map:
            raise ValueError("Malformed input: root reference invalid")
        return obj_map[rid]
    # primitive root
    if root is None or isinstance(root, (bool, int, float, str)):
        return root
    # anything else is malformed
    raise ValueError("Malformed input: invalid root")
