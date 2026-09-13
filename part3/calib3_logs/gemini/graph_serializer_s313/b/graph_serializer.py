
import json

def encode(obj: object) -> str:
    """
    Serializes a Python object graph to a string, preserving shared references and cycles.
    """
    memo = {}  # Maps id(obj) to its index in the flat_graph
    flat_graph = []

    def _encode_recursive(o):
        obj_id = id(o)
        if obj_id in memo:
            return memo[obj_id]

        # Placeholder for the object to handle cycles
        index = len(flat_graph)
        memo[obj_id] = index
        flat_graph.append(None)

        serialized_obj = {}
        if o is None or isinstance(o, (bool, int, float, str)):
            serialized_obj['type'] = 'primitive'
            serialized_obj['value'] = o
        elif isinstance(o, list):
            serialized_obj['type'] = 'list'
            serialized_obj['value'] = [_encode_recursive(item) for item in o]
        elif isinstance(o, dict):
            if not all(isinstance(k, str) for k in o.keys()):
                raise ValueError("Dictionary keys must be strings.")
            serialized_obj['type'] = 'dict'
            serialized_obj['value'] = {k: _encode_recursive(v) for k, v in o.items()}
        else:
            raise ValueError(f"Unsupported type: {type(o).__name__}")

        flat_graph[index] = serialized_obj
        return index

    if obj is not None:
        _encode_recursive(obj)
        
    return json.dumps(flat_graph)

def decode(s: str) -> object:
    """
    Deserializes a string back into a Python object graph, restoring shared references and cycles.
    """
    try:
        flat_graph = json.loads(s)
    except json.JSONDecodeError:
        raise ValueError("Malformed input: Not valid JSON.")

    if not isinstance(flat_graph, list):
        raise ValueError("Malformed input: Expected a JSON list.")

    if not flat_graph:
        return None

    memo = {}  # Maps index to the reconstructed object

    # Pass 1: Create placeholder objects
    for i, serialized_obj in enumerate(flat_graph):
        if not isinstance(serialized_obj, dict) or 'type' not in serialized_obj:
            raise ValueError(f"Malformed object at index {i}")
            
        obj_type = serialized_obj['type']
        if obj_type == 'primitive':
            memo[i] = serialized_obj.get('value')
        elif obj_type == 'list':
            memo[i] = []
        elif obj_type == 'dict':
            memo[i] = {}
        else:
            raise ValueError(f"Unknown object type '{obj_type}' at index {i}")

    # Pass 2: Populate the placeholder objects
    for i, serialized_obj in enumerate(flat_graph):
        obj_type = serialized_obj['type']
        reconstructed_obj = memo[i]

        if obj_type == 'list':
            item_ids = serialized_obj.get('value', [])
            if not isinstance(item_ids, list):
                 raise ValueError(f"Malformed list value at index {i}")
            for item_id in item_ids:
                if not isinstance(item_id, int) or item_id not in memo:
                    raise ValueError(f"Invalid object reference '{item_id}' in list at index {i}")
                reconstructed_obj.append(memo[item_id])
        elif obj_type == 'dict':
            item_map = serialized_obj.get('value', {})
            if not isinstance(item_map, dict):
                 raise ValueError(f"Malformed dict value at index {i}")
            for key, value_id in item_map.items():
                if not isinstance(value_id, int) or value_id not in memo:
                    raise ValueError(f"Invalid object reference '{value_id}' in dict at index {i}")
                reconstructed_obj[key] = memo[value_id]

    return memo.get(0)
