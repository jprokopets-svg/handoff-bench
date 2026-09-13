
import json

def encode(obj):
    """
    Serializes a Python object graph to a JSON string, preserving shared
    references and cycles.
    """
    memo = {}  # id(obj) -> index in graph
    graph = [] # All unique containers

    def _traverse(o):
        obj_id = id(o)
        if obj_id in memo:
            return {"$ref": memo[obj_id]}

        if isinstance(o, (int, float, bool, str, type(None))):
            return o

        if not isinstance(o, (list, dict)):
            raise ValueError(f"Unsupported type: {type(o).__name__}")

        # It's a new container, assign an ID and add a placeholder.
        index = len(graph)
        memo[obj_id] = index
        graph.append(None)

        if isinstance(o, list):
            representation = [_traverse(item) for item in o]
        elif isinstance(o, dict):
            for key in o:
                if not isinstance(key, str):
                    raise ValueError("Dictionary keys must be strings.")
            representation = {k: _traverse(v) for k, v in o.items()}
        
        graph[index] = representation
        return {"$ref": index}

    # The root might be a primitive, so we can't just assume it's a ref.
    root_representation = _traverse(obj)
    
    return json.dumps({"root": root_representation, "graph": graph})


def decode(s):
    """
    Deserializes a JSON string created by encode() back into a Python
    object graph, reconstructing shared references and cycles.
    """
    try:
        data = json.loads(s)
        if not isinstance(data, dict) or "root" not in data or "graph" not in data:
            raise ValueError("Invalid serialization format")
        graph_repr = data['graph']
        root_repr = data['root']
    except (json.JSONDecodeError, TypeError):
        raise ValueError("Malformed input string")

    memo = {}  # index -> reconstructed object

    # 1st pass: Create empty objects for all containers.
    for i, representation in enumerate(graph_repr):
        if isinstance(representation, list):
            memo[i] = []
        elif isinstance(representation, dict):
            memo[i] = {}
        else:
            # This should not happen if the input is valid, as only
            # containers are placed in the graph list.
            raise ValueError("Invalid item in graph list")

    def _reconstruct(value_repr):
        if isinstance(value_repr, dict) and "$ref" in value_repr:
            return memo[value_repr["$ref"]]
        
        # It's a primitive value
        if isinstance(value_repr, (int, float, bool, str, type(None))):
            return value_repr
        
        # This handles the case where the root is a container but not part of a cycle
        # (e.g., encode([1,2,3])). It won't have a $ref.
        if isinstance(value_repr, list):
            return [_reconstruct(item) for item in value_repr]
        if isinstance(value_repr, dict):
            return {k: _reconstruct(v) for k,v in value_repr.items()}

        raise ValueError(f"Invalid value representation: {value_repr}")


    # 2nd pass: Populate the empty objects.
    for i, representation in enumerate(graph_repr):
        obj = memo[i]
        if isinstance(obj, list):
            obj.extend(_reconstruct(item) for item in representation)
        elif isinstance(obj, dict):
            for k, v_repr in representation.items():
                obj[k] = _reconstruct(v_repr)

    return _reconstruct(root_repr)
