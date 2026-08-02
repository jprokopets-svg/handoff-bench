import json
from typing import Any, Union

def encode(obj: object) -> str:
    """Serialize object graph to a string preserving shared references and cycles."""
    memo = {}  # id(obj) -> (obj_id, serialized)
    next_id = 0
    obj_to_id = {}  # id(obj) -> assigned integer id

    def _encode(obj: Any) -> Any:
        nonlocal next_id
        obj_id = id(obj)
        if obj_id in obj_to_id:
            # already assigned an id, return reference
            return {'$ref': obj_to_id[obj_id]}

        # assign new id
        my_id = next_id
        next_id += 1
        obj_to_id[obj_id] = my_id

        # handle primitive types
        if obj is None:
            return {'$type': 'null', '$id': my_id}
        if isinstance(obj, bool):
            return {'$type': 'bool', '$value': obj, '$id': my_id}
        if isinstance(obj, int):
            return {'$type': 'int', '$value': obj, '$id': my_id}
        if isinstance(obj, float):
            return {'$type': 'float', '$value': obj, '$id': my_id}
        if isinstance(obj, str):
            return {'$type': 'str', '$value': obj, '$id': my_id}
        if isinstance(obj, list):
            # first create placeholder with id, then encode children
            result = {'$type': 'list', '$id': my_id, '$items': []}
            # store placeholder early so recursive calls can refer to this list
            memo[my_id] = result
            # encode each child
            for item in obj:
                result['$items'].append(_encode(item))
            return result
        if isinstance(obj, dict):
            # check keys are strings
            for key in obj.keys():
                if not isinstance(key, str):
                    raise ValueError('dict keys must be strings')
            result = {'$type': 'dict', '$id': my_id, '$items': []}
            memo[my_id] = result
            for key, value in obj.items():
                result['$items'].append([key, _encode(value)])
            return result
        raise ValueError('unsupported type')

    encoded = _encode(obj)
    # The encoded structure may contain references to objects not yet fully serialized,
    # but that's okay because we have placeholders.
    return json.dumps(encoded, ensure_ascii=False)


def decode(s: str) -> object:
    """Deserialize string back to object graph preserving shared references and cycles."""
    try:
        data = json.loads(s)
    except json.JSONDecodeError:
        raise ValueError('malformed input')

    # map from id to reconstructed object
    id_to_obj = {}

    def _decode(node: Any) -> Any:
        if isinstance(node, dict):
            if '$ref' in node:
                # reference to existing object
                ref_id = node['$ref']
                if ref_id not in id_to_obj:
                    raise ValueError('reference to undefined object')
                return id_to_obj[ref_id]
            if '$type' not in node:
                raise ValueError('missing $type')
            node_type = node['$type']
            node_id = node.get('$id')
            if node_id is None:
                raise ValueError('missing $id')
            if node_type == 'null':
                obj = None
            elif node_type == 'bool':
                obj = node['$value']
            elif node_type == 'int':
                obj = node['$value']
            elif node_type == 'float':
                obj = node['$value']
            elif node_type == 'str':
                obj = node['$value']
            elif node_type == 'list':
                # create list placeholder
                obj = []
                id_to_obj[node_id] = obj
                items = node.get('$items', [])
                # decode each child
                for item in items:
                    obj.append(_decode(item))
                return obj
            elif node_type == 'dict':
                obj = {}
                id_to_obj[node_id] = obj
                items = node.get('$items', [])
                for key, value_node in items:
                    if not isinstance(key, str):
                        raise ValueError('dict key must be string')
                    obj[key] = _decode(value_node)
                return obj
            else:
                raise ValueError('unknown type')
            # for primitive types, store mapping (though they are immutable)
            id_to_obj[node_id] = obj
            return obj
        else:
            # primitive value not wrapped? shouldn't happen
            raise ValueError('unexpected value')

    return _decode(data)