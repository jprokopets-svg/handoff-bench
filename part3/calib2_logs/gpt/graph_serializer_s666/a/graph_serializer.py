import json


def encode(obj):
    """Serialize object graph preserving shared references and cycles.
    Supported types: int, float, bool, None, str, list, dict (string keys).
    Returns a JSON string representing the graph.
    """
    # First pass: traverse and assign ids
    id_map = {}  # id(obj) -> assigned id
    id_to_obj = []
    stack = [obj]
    while stack:
        cur = stack.pop()
        oid = id(cur)
        if oid in id_map:
            continue
        # type checks
        if isinstance(cur, bool):
            pass
        elif cur is None:
            pass
        elif isinstance(cur, int):
            pass
        elif isinstance(cur, float):
            pass
        elif isinstance(cur, str):
            pass
        elif isinstance(cur, list):
            pass
        elif isinstance(cur, dict):
            # ensure keys are strings
            for k in cur.keys():
                if not isinstance(k, str):
                    raise ValueError("dict keys must be strings")
        else:
            raise ValueError(f"Unsupported type: {type(cur)}")
        assigned = len(id_to_obj)
        id_map[oid] = assigned
        id_to_obj.append(cur)
        # push children for traversal
        if isinstance(cur, list):
            for el in cur:
                stack.append(el)
        elif isinstance(cur, dict):
            for v in cur.values():
                stack.append(v)

    # Second pass: build serializable nodes
    nodes = []
    for cur in id_to_obj:
        if isinstance(cur, bool):
            node = {"t": "bool", "v": cur}
        elif cur is None:
            node = {"t": "null", "v": None}
        elif isinstance(cur, int):
            node = {"t": "int", "v": cur}
        elif isinstance(cur, float):
            node = {"t": "float", "v": cur}
        elif isinstance(cur, str):
            node = {"t": "str", "v": cur}
        elif isinstance(cur, list):
            ids = [id_map[id(el)] for el in cur]
            node = {"t": "list", "v": ids}
        elif isinstance(cur, dict):
            m = {k: id_map[id(v)] for k, v in cur.items()}
            node = {"t": "dict", "v": m}
        else:
            # should not happen
            raise ValueError(f"Unsupported type during emit: {type(cur)}")
        nodes.append(node)

    root_id = id_map[id(obj)]
    out = {"root": root_id, "nodes": nodes}
    return json.dumps(out, ensure_ascii=False, separators=(',', ':'))


def decode(s):
    """Decode string produced by encode back into object graph, preserving identity and cycles."""
    try:
        data = json.loads(s)
    except Exception as e:
        raise ValueError("Malformed input") from e
    if not isinstance(data, dict):
        raise ValueError("Malformed input: root object must be a dict")
    if 'root' not in data or 'nodes' not in data:
        raise ValueError("Malformed input: missing keys")
    root = data['root']
    nodes = data['nodes']
    if not isinstance(root, int):
        raise ValueError("Malformed input: root must be int")
    if not isinstance(nodes, list):
        raise ValueError("Malformed input: nodes must be list")
    n = len(nodes)
    if not (0 <= root < n):
        raise ValueError("Malformed input: root out of range")
    # Validate node shapes and create placeholders
    placeholders = [None] * n
    # We'll store node types/values for second pass
    node_types = [None] * n
    node_vals = [None] * n
    for i, node in enumerate(nodes):
        if not isinstance(node, dict):
            raise ValueError("Malformed input: node must be dict")
        if 't' not in node or 'v' not in node:
            raise ValueError("Malformed input: node missing t/v")
        t = node['t']
        v = node['v']
        node_types[i] = t
        node_vals[i] = v
        if t == 'list':
            if not isinstance(v, list):
                raise ValueError("Malformed input: list node v must be list")
            placeholders[i] = []
        elif t == 'dict':
            if not isinstance(v, dict):
                raise ValueError("Malformed input: dict node v must be dict")
            # keys must be strings
            for k in v.keys():
                if not isinstance(k, str):
                    raise ValueError("Malformed input: dict keys must be strings")
            placeholders[i] = {}
        elif t == 'int':
            if not isinstance(v, int):
                # JSON may decode ints as int, floats as float; ensure int
                raise ValueError("Malformed input: int node v must be int")
            placeholders[i] = v
        elif t == 'float':
            if not isinstance(v, (int, float)):
                raise ValueError("Malformed input: float node v must be number")
            # ensure float type
            placeholders[i] = float(v)
        elif t == 'bool':
            if not isinstance(v, bool):
                raise ValueError("Malformed input: bool node v must be bool")
            placeholders[i] = v
        elif t == 'null':
            if v is not None:
                raise ValueError("Malformed input: null node v must be null")
            placeholders[i] = None
        elif t == 'str':
            if not isinstance(v, str):
                raise ValueError("Malformed input: str node v must be string")
            placeholders[i] = v
        else:
            raise ValueError(f"Malformed input: unknown node type {t}")
    # Second pass: fill list and dict contents
    for i in range(n):
        t = node_types[i]
        v = node_vals[i]
        if t == 'list':
            lst = placeholders[i]
            for child_idx in v:
                if not isinstance(child_idx, int) or not (0 <= child_idx < n):
                    raise ValueError("Malformed input: invalid child index in list")
                lst.append(placeholders[child_idx])
        elif t == 'dict':
            d = placeholders[i]
            for k, child_idx in v.items():
                if not isinstance(child_idx, int) or not (0 <= child_idx < n):
                    raise ValueError("Malformed input: invalid child index in dict")
                d[k] = placeholders[child_idx]
    return placeholders[root]
