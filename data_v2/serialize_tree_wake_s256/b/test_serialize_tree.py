import pytest
from serialize_tree import TreeNode, serialize, deserialize


def test_serialize_empty_tree():
    """Test serializing an empty tree."""
    assert serialize(None) == ""


def test_deserialize_empty_tree():
    """Test deserializing an empty string."""
    assert deserialize("") is None


def test_serialize_single_node():
    """Test serializing a tree with a single node."""
    root = TreeNode(1)
    assert serialize(root) == "1"


def test_deserialize_single_node():
    """Test deserializing a single node."""
    root = deserialize("1")
    assert root.val == 1
    assert root.left is None
    assert root.right is None


def test_serialize_complete_tree():
    """Test serializing a complete binary tree."""
    #       1
    #      / \
    #     2   3
    #    / \
    #   4   5
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    
    serialized = serialize(root)
    assert serialized == "1,2,3,4,5"


def test_deserialize_complete_tree():
    """Test deserializing a complete binary tree."""
    serialized = "1,2,3,4,5"
    root = deserialize(serialized)
    
    assert root.val == 1
    assert root.left.val == 2
    assert root.right.val == 3
    assert root.left.left.val == 4
    assert root.left.right.val == 5
    assert root.right.left is None
    assert root.right.right is None


def test_serialize_tree_with_nulls():
    """Test serializing a tree with missing nodes."""
    #       1
    #      / \
    #     2   null
    #    / \
    #   4   5
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    
    serialized = serialize(root)
    assert serialized == "1,2,null,4,5"


def test_deserialize_tree_with_nulls():
    """Test deserializing a tree with null nodes."""
    serialized = "1,2,null,4,5"
    root = deserialize(serialized)
    
    assert root.val == 1
    assert root.left.val == 2
    assert root.right is None
    assert root.left.left.val == 4
    assert root.left.right.val == 5


def test_serialize_deserialize_roundtrip():
    """Test that serialize and deserialize are inverses."""
    #       1
    #      / \
    #     2   3
    #    /     \
    #   4       5
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.right.right = TreeNode(5)
    
    serialized = serialize(root)
    deserialized = deserialize(serialized)
    
    # Verify structure
    assert deserialized.val == 1
    assert deserialized.left.val == 2
    assert deserialized.right.val == 3
    assert deserialized.left.left.val == 4
    assert deserialized.left.right is None
    assert deserialized.right.left is None
    assert deserialized.right.right.val == 5


def test_serialize_left_skewed_tree():
    """Test serializing a left-skewed tree."""
    #     1
    #    /
    #   2
    #  /
    # 3
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.left.left = TreeNode(3)
    
    serialized = serialize(root)
    assert serialized == "1,2,null,3"


def test_deserialize_left_skewed_tree():
    """Test deserializing a left-skewed tree."""
    serialized = "1,2,null,3"
    root = deserialize(serialized)
    
    assert root.val == 1
    assert root.left.val == 2
    assert root.right is None
    assert root.left.left.val == 3
    assert root.left.right is None


def test_serialize_right_skewed_tree():
    """Test serializing a right-skewed tree."""
    #   1
    #    \
    #     2
    #      \
    #       3
    root = TreeNode(1)
    root.right = TreeNode(2)
    root.right.right = TreeNode(3)
    
    serialized = serialize(root)
    assert serialized == "1,null,2,null,3"


def test_deserialize_right_skewed_tree():
    """Test deserializing a right-skewed tree."""
    serialized = "1,null,2,null,3"
    root = deserialize(serialized)
    
    assert root.val == 1
    assert root.left is None
    assert root.right.val == 2
    assert root.right.left is None
    assert root.right.right.val == 3


def test_serialize_tree_with_negative_values():
    """Test serializing a tree with negative values."""
    root = TreeNode(-1)
    root.left = TreeNode(-2)
    root.right = TreeNode(3)
    
    serialized = serialize(root)
    assert serialized == "-1,-2,3"


def test_deserialize_tree_with_negative_values():
    """Test deserializing a tree with negative values."""
    serialized = "-1,-2,3"
    root = deserialize(serialized)
    
    assert root.val == -1
    assert root.left.val == -2
    assert root.right.val == 3
