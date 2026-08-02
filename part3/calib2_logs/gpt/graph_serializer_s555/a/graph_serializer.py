import json


class _Sentinel:
    pass


def encode(obj):
    # Build graph nodes with unique ids preserving identity
    obj_to_uid = {}
    nodes = []  # list of dicts {"t": type, "v": value}

    def get_uid_for(o):
        oid = id(o)
        if oid in obj_to_uid:
            return obj_to_uid[oid]
        uid = len(nodes)
        obj_to_uid[oid] = uid
        nodes.append({"t": None, "v": None})  # placeholder
        _serialize(o, uid)
        return uid

    def _serialize(o, uid):
        # determine type and fill nodes[uid]
        # order of isinstance checks matters: bool is subclass of int
        if o is None:
            nodes[uid]["t"] = "none"
            nodes[uid]["v"] = None
        elif isinstance(o, bool):
            nodes[uid]["t"] = "bool"
            nodes[uid]["v"] = o
        elif isinstance(o, int):
            nodes[uid]["t"] = "int"
            nodes[uid]["v"] = o
        elif isinstance(o, float):
            nodes[uid]["t"] = "float"
            nodes[uid]["v"] = o
        elif isinstance(o, str):
            nodes[uid]["t"] = "str"
            nodes[uid]["v"] = o
        elif isinstance(o, list):
            nodes[uid]["t"] = "list"
            # create list of uids
            vals = []
            nodes[uid]["v"] = vals
            for item in o:
                vals.append(get_uid_for(item))
        elif isinstance(o, dict):
            # keys must be strings
            for k in o.keys():
                if not isinstance(k, str):
                    raise ValueError("Unsupported dict key type")
            nodes[uid]["t"] = "dict"
            mapping = {}
            nodes[uid]["v"] = mapping
            for k, v in o.items():
                mapping[k] = get_uid_for(v)
        else:
            raise ValueError(f"Unsupported type: {type(o)}")

    root_uid = get_uid_for(obj)
    # Prepare serializable structure: convert uid ints to strings for JSON keys
    objects = {}
    for uid, node in enumerate(nodes):
        # Node must be a dict with t and v
        t = node["t"]
        v = node["v"]
        # For list and dict, ensure their v contains ints (uids)
        objects[str(uid)] = {"t": t, "v": v}
    data = {"root": str(root_uid), "objects": objects}
    return json.dumps(data, separators=(",",":"), ensure_ascii=False)


def decode(s):
    try:
        data = json.loads(s)
    except Exception:
        raise ValueError("Malformed input")
    if not isinstance(data, dict):
        raise ValueError("Malformed input: root must be object")
    if "root" not in data or "objects" not in data:
        raise ValueError("Malformed input: missing keys")
    root = data["root"]
    objects = data["objects"]
    if not isinstance(objects, dict):
        raise ValueError("Malformed input: objects must be dict")
    # Build placeholder list for uids
    # UIDs are keys of objects dict, expected as strings that represent integers 0..n-1 but order may vary
    # We'll map uid_str -> index int
    uid_strs = list(objects.keys())
    # Validate uid strings are integers >=0
    uid_ints = {}
    for ustr in uid_strs:
        if not isinstance(ustr, str):
            raise ValueError("Malformed input: invalid uid key")
        try:
            ui = int(ustr)
        except Exception:
            raise ValueError("Malformed input: invalid uid key")
        if ui < 0:
            raise ValueError("Malformed input: invalid uid key")
        uid_ints[ustr] = ui
    # Create a list of size max_uid+1 initialized to sentinel
    max_uid = max(uid_ints.values()) if uid_ints else -1
    objs = [_Sentinel] * (max_uid + 1)

    # First pass: validate node structure and create placeholders for list/dict, and primitives values
    node_entries = {}
    for ustr, node in objects.items():
        ui = uid_ints[ustr]
        if not isinstance(node, dict):
            raise ValueError("Malformed input: node must be object")
        if "t" not in node or "v" not in node:
            raise ValueError("Malformed input: node missing keys")
        t = node["t"]
        v = node["v"]
        node_entries[ui] = (t, v)
        # allocate placeholder or final value
        if t == "list":
            objs[ui] = []
        elif t == "dict":
            objs[ui] = {}
        elif t == "int":
            if not isinstance(v, int):
                raise ValueError("Malformed input: int value expected")
            objs[ui] = v
        elif t == "float":
            # JSON may parse floats as int if integer-looking? json uses int vs float; but floats will be float
            if not (isinstance(v, float) or isinstance(v, int)):
                # allow ints for floats? if original float was integral, json still encodes as number; json loads as int
                raise ValueError("Malformed input: float value expected")
            objs[ui] = float(v)
        elif t == "bool":
            if not isinstance(v, bool):
                raise ValueError("Malformed input: bool value expected")
            objs[ui] = v
        elif t == "none":
            if v is not None:
                raise ValueError("Malformed input: none value expected")
            objs[ui] = None
        elif t == "str":
            if not isinstance(v, str):
                raise ValueError("Malformed input: str value expected")
            objs[ui] = v
        else:
            raise ValueError("Malformed input: unknown type")

    # Second pass: fill list and dict contents
    for ui, (t, v) in node_entries.items():
        if t == "list":
            if not isinstance(v, list):
                raise ValueError("Malformed input: list value expected")
            lst = objs[ui]
            for ref in v:
                if not (isinstance(ref, int) or isinstance(ref, str)):
                    raise ValueError("Malformed input: invalid reference")
                # ref may be int or string (we used ints in encode), convert to int
                try:
                    rid = int(ref)
                except Exception:
                    raise ValueError("Malformed input: invalid reference id")
                if rid < 0 or rid > max_uid or objs[rid] is _Sentinel:
                    raise ValueError("Malformed input: reference to unknown uid")
                lst.append(objs[rid])
        elif t == "dict":
            if not isinstance(v, dict):
                raise ValueError("Malformed input: dict value expected")
            dct = objs[ui]
            for k, ref in v.items():
                if not isinstance(k, str):
                    raise ValueError("Malformed input: dict key must be string")
                if not (isinstance(ref, int) or isinstance(ref, str)):
                    raise ValueError("Malformed input: invalid reference")
                try:
                    rid = int(ref)
                except Exception:
                    raise ValueError("Malformed input: invalid reference id")
                if rid < 0 or rid > max_uid or objs[rid] is _Sentinel:
                    raise ValueError("Malformed input: reference to unknown uid")
                dct[k] = objs[rid]

    # Resolve root
    try:
        root_id = int(root)
    except Exception:
        raise ValueError("Malformed input: invalid root id")
    if root_id < 0 or root_id > max_uid or objs[root_id] is _Sentinel:
        raise ValueError("Malformed input: root refers to unknown uid")
    return objs[root_id]
