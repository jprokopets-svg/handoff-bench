from serialize_tree import *

def test_serialize_deserialize():
    root = deserialize('[1,2,3,null,null,4,5]')
    assert serialize(root) == '[1,2,3,null,null,4,5]'

def test_empty_tree():
    root = deserialize('[]')
    assert serialize(root) == '[]'

def test_single_node():
    root = deserialize('[1]')
    assert serialize(root) == '[1]'
