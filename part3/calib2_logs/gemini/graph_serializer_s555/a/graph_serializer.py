
import json

class GraphSerializer:
    def __init__(self):
        self.objects = []  # Stores the actual Python objects during encoding/decoding
        self.id_map = {}   # Maps object IDs to their index in self.objects

    def encode(self, obj):
        self.objects = []
        self.id_map = {}
        # The result of the first recursive call is the root object's representation
        # We need to store the actual object in self.objects for reference tracking
        # and then return the index of the root object.
        self._encode_recursive(obj)
        return json.dumps(self.objects)

    def _encode_recursive(self, obj):
        obj_id = id(obj)
        if obj_id in self.id_map:
            return {"__ref__": self.id_map[obj_id]}

        idx = len(self.objects)
        self.id_map[obj_id] = idx
        # Placeholder for the object, will be updated later for lists/dicts
        self.objects.append(None)

        if isinstance(obj, (int, float, bool, type(None), str)):
            self.objects[idx] = obj
            return obj
        elif isinstance(obj, list):
            # Store a list of encoded references/values
            encoded_list_content = []
            self.objects[idx] = {"__list__": encoded_list_content}
            for item in obj:
                encoded_list_content.append(self._encode_recursive(item))
            return {"__ref__": idx} # Return a reference to this list
        elif isinstance(obj, dict):
            # Store a dict of encoded references/values
            encoded_dict_content = {}
            self.objects[idx] = {"__dict__": encoded_dict_content}
            for key, value in obj.items():
                if not isinstance(key, str):
                    raise ValueError("Dict keys must be strings.")
                encoded_dict_content[key] = self._encode_recursive(value)
            return {"__ref__": idx} # Return a reference to this dict
        else:
            raise ValueError(f"Unsupported type: {type(obj)}")

    def decode(self, s):
        serialized_objects = json.loads(s)
        self.objects = [None] * len(serialized_objects)

        # First pass: create all objects (empty lists/dicts or primitives)
        for i, item_repr in enumerate(serialized_objects):
            if isinstance(item_repr, dict) and "__list__" in item_repr:
                self.objects[i] = []
            elif isinstance(item_repr, dict) and "__dict__" in item_repr:
                self.objects[i] = {}
            else:
                self.objects[i] = item_repr

        # Second pass: populate lists and dicts, resolving references
        for i, item_repr in enumerate(serialized_objects):
            if isinstance(item_repr, dict) and "__list__" in item_repr:
                decoded_list = self.objects[i]
                for encoded_item in item_repr["__list__"]:
                    decoded_list.append(self._decode_recursive(encoded_item))
            elif isinstance(item_repr, dict) and "__dict__" in item_repr:
                decoded_dict = self.objects[i]
                for key, encoded_value in item_repr["__dict__"].items():
                    decoded_dict[key] = self._decode_recursive(encoded_value)
        
        return self.objects[0]

    def _decode_recursive(self, encoded_obj):
        if isinstance(encoded_obj, dict) and "__ref__" in encoded_obj:
            return self.objects[encoded_obj["__ref__"]]
        # If it's not a reference, it must be a primitive value or a nested list/dict that
        # has already been created in the first pass of decode.
        # However, the current structure of `serialized_objects` means that
        # `encoded_obj` here will either be a primitive or a `{"__ref__": idx}`.
        # The actual list/dict content is in `serialized_objects[idx]`.
        # So, if it's not a ref, it's a primitive.
        return encoded_obj

serializer = GraphSerializer()
encode = serializer.encode
decode = serializer.decode
