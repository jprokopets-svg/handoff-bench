import pytest
from serialize_tree import TreeNode, serialize, deserialize


class TestSerializeTree:
    """Test cases for tree serialization and deserialization."""
    
    def test_empty_tree(self):
        """Test serializing and deserializing an empty tree."""
        root = None
        serialized = serialize(root)
        assert serialized == ""
        deserialized = deserialize(serialized)
        assert deserialized is None
    
    def test_single_node(self):
        """Test serializing and deserializing a single node tree."""
        root = TreeNode(1)
        serialized = serialize(root)
        assert serialized == "1"
        deserialized = deserialize(serialized)
        assert deserialized.val == 1
        assert deserialized.left is None
        assert deserialized.right is None
    
    def test_complete_binary_tree(self):
        """Test serializing and deserializing a complete binary tree."""
        # Tree structure:
        #       1
        #      / \
        #     2   3
        #    / \ / \
        #   4  5 6  7
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        root.left.left = TreeNode(4)
        root.left.right = TreeNode(5)
        root.right.left = TreeNode(6)
        root.right.right = TreeNode(7)
        
        serialized = serialize(root)
        assert serialized == "1,2,3,4,5,6,7"
        
        deserialized = deserialize(serialized)
        assert deserialized.val == 1
        assert deserialized.left.val == 2
        assert deserialized.right.val == 3
        assert deserialized.left.left.val == 4
        assert deserialized.left.right.val == 5
        assert deserialized.right.left.val == 6
        assert deserialized.right.right.val == 7
    
    def test_tree_with_nulls(self):
        """Test serializing and deserializing a tree with missing nodes."""
        # Tree structure:
        #       1
        #      / \
        #     2   null
        #    / \
        #   3   4
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.left.left = TreeNode(3)
        root.left.right = TreeNode(4)
        
        serialized = serialize(root)
        assert serialized == "1,2,null,3,4"
        
        deserialized = deserialize(serialized)
        assert deserialized.val == 1
        assert deserialized.left.val == 2
        assert deserialized.right is None
        assert deserialized.left.left.val == 3
        assert deserialized.left.right.val == 4
    
    def test_left_skewed_tree(self):
        """Test serializing and deserializing a left-skewed tree."""
        # Tree structure:
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
        
        deserialized = deserialize(serialized)
        assert deserialized.val == 1
        assert deserialized.left.val == 2
        assert deserialized.right is None
        assert deserialized.left.left.val == 3
        assert deserialized.left.right is None
    
    def test_right_skewed_tree(self):
        """Test serializing and deserializing a right-skewed tree."""
        # Tree structure:
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
        
        deserialized = deserialize(serialized)
        assert deserialized.val == 1
        assert deserialized.left is None
        assert deserialized.right.val == 2
        assert deserialized.right.left is None
        assert deserialized.right.right.val == 3
    
    def test_round_trip(self):
        """Test that serialize -> deserialize -> serialize produces the same result."""
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        root.left.left = TreeNode(4)
        root.right.right = TreeNode(5)
        
        serialized1 = serialize(root)
        deserialized = deserialize(serialized1)
        serialized2 = serialize(deserialized)
        
        assert serialized1 == serialized2
    
    def test_negative_values(self):
        """Test serializing and deserializing trees with negative values."""
        root = TreeNode(-1)
        root.left = TreeNode(-2)
        root.right = TreeNode(3)
        
        serialized = serialize(root)
        assert serialized == "-1,-2,3"
        
        deserialized = deserialize(serialized)
        assert deserialized.val == -1
        assert deserialized.left.val == -2
        assert deserialized.right.val == 3
