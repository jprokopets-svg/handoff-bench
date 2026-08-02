import json

class GraphSerializer:
    def __init__(self):
        self.encoding_id_map = {}  # Maps id(obj) to an integer ID during encoding
        self.encoded_objects = []  # Stores the encoded representation of objects during encoding

        self.decoded_objects = []  # Stores actual Python objects during decoding
        self.id_to_object_map = {} # Maps integer ID to actual Python obj during decoding

    def encode(self, obj):
        self.encoding_id_map = {}
        self.encoded_objects = []
        
        encoded_root_ref = self._encode_recursive(obj)
        
        return json.dumps({"root": encoded_root_ref, "objects": self.encoded_objects})

    def _encode_recursive(self, obj):
        if id(obj) in self.encoding_id_map:
            return {"__ref__": self.encoding_id_map[id(obj)]}

        obj_id = len(self.encoded_objects)
        self.encoding_id_map[id(obj)] = obj_id
        
        self.encoded_objects.append(None) 

        if isinstance(obj, (int, float, bool, type(None), str)):
            self.encoded_objects[obj_id] = obj
            return obj
        elif isinstance(obj, list):
            self.encoded_objects[obj_id] = {"__list__": []} 
            
            encoded_elements = [self._encode_recursive(item) for item in obj]
            
            self.encoded_objects[obj_id]["__list__"] = encoded_elements
            return {"__ref__": obj_id} 
        elif isinstance(obj, dict):
            self.encoded_objects[obj_id] = {"__dict__": {}} 

            encoded_items = {k: self._encode_recursive(v) for k, v in obj.items()}
            
            self.encoded_objects[obj_id]["__dict__"] = encoded_items
            return {"__ref__": obj_id} 
        else:
            raise ValueError(f"Unsupported type: {type(obj)}")

    def decode(self, s):
        self.decoded_objects = []
        self.id_to_object_map = {}

        data = json.loads(s)
        encoded_root_ref = data["root"]
        self.encoded_objects = data["objects"] 

        self._decode_create_placeholders()
        
        # Populate all objects created in the first pass
        for obj_id, _ in enumerate(self.encoded_objects):
            if obj_id in self.id_to_object_map: # Only populate complex objects
                self._populate_single_object(obj_id)

        # Finally, return the root object
        if isinstance(encoded_root_ref, dict) and "__ref__" in encoded_root_ref:
            return self.id_to_object_map[encoded_root_ref["__ref__"]]
        else:
            return encoded_root_ref

    def _decode_create_placeholders(self):
        for obj_id, encoded_obj in enumerate(self.encoded_objects):
            if isinstance(encoded_obj, dict):
                if "__list__" in encoded_obj:
                    new_list = []
                    # We don't need to append to decoded_objects here, id_to_object_map is enough
                    self.id_to_object_map[obj_id] = new_list
                elif "__dict__" in encoded_obj:
                    new_dict = {}
                    # We don't need to append to decoded_objects here, id_to_object_map is enough
                    self.id_to_object_map[obj_id] = new_dict
            elif not isinstance(encoded_obj, (int, float, bool, type(None), str)):
                raise ValueError(f"Malformed encoded object during placeholder creation: {encoded_obj}")

    def _populate_single_object(self, obj_id):
        encoded_obj = self.encoded_objects[obj_id]
        decoded_obj = self.id_to_object_map[obj_id]

        if "__list__" in encoded_obj:
            for item_encoded in encoded_obj["__list__"]:
                if isinstance(item_encoded, dict) and "__ref__" in item_encoded:
                    decoded_obj.append(self.id_to_object_map[item_encoded["__ref__"]])
                else:
                    decoded_obj.append(item_encoded)
        elif "__dict__" in encoded_obj:
            for key, value_encoded in encoded_obj["__dict__"].items():
                if isinstance(value_encoded, dict) and "__ref__" in value_encoded:
                    decoded_obj[key] = self.id_to_object_map[value_encoded["__ref__"]]
                else:
                    decoded_obj[key] = value_encoded

serializer = GraphSerializer()
encode = serializer.encode
decode = serializer.decode
