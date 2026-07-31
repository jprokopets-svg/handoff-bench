import pytest
from serialize_tree import TreeNode, serialize, deserialize


class TestSerializeTree:
    """Test cases for binary tree serialization and deserialization."""
    
    def test_empty_tree(self):
        """Test serialization and deserialization of empty tree."""
        assert serialize(None) == ""
        assert deserialize("") is None
    
    def test_single_node(self):
        """Test serialization and deserialization of single node tree."""
        root = TreeNode(1)
        serialized = serialize(root)
        assert serialized == "1"
        
        deserialized = deserialize(serialized)
        assert deserialized.val == 1
        assert deserialized.left is None
        assert deserialized.right is None
    
    def test_simple_tree(self):
        """Test serialization and deserialization of simple tree."""
        #     1
        #    / \
        #   2   3
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        
        serialized = serialize(root)
        assert serialized == "1,2,3"
        
        deserialized = deserialize(serialized)
        assert deserialized.val == 1
        assert deserialized.left.val == 2
        assert deserialized.right.val == 3
        assert deserialized.left.left is None
        assert deserialized.left.right is None
        assert deserialized.right.left is None
        assert deserialized.right.right is None
    
    def test_tree_with_nulls(self):
        """Test serialization and deserialization of tree with missing nodes."""
        #     1
        #    / \
        #   2   null
        #  / \
        # 3   4
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
    
    def test_skewed_tree_left(self):
        """Test serialization and deserialization of left-skewed tree."""
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
    
    def test_skewed_tree_right(self):
        """Test serialization and deserialization of right-skewed tree."""
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
    
    def test_negative_values(self):
        """Test serialization and deserialization with negative values."""
        root = TreeNode(-1)
        root.left = TreeNode(-2)
        root.right = TreeNode(3)
        
        serialized = serialize(root)
        assert serialized == "-1,-2,3"
        
        deserialized = deserialize(serialized)
        assert deserialized.val == -1
        assert deserialized.left.val == -2
        assert deserialized.right.val == 3
    
    def test_round_trip(self):
        """Test that serialize -> deserialize -> serialize produces same result."""
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
        
        serialized1 = serialize(root)
        deserialized = deserialize(serialized1)
        serialized2 = serialize(deserialized)
        
        assert serialized1 == serialized2
    
    def test_complex_tree(self):
        """Test serialization and deserialization of complex tree."""
        #         1
        #       /   \
        #      2     3
        #     / \   / \
        #    4   5 6   7
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
    
    def test_tree_with_zeros(self):
        """Test serialization and deserialization with zero values."""
        root = TreeNode(0)
        root.left = TreeNode(0)
        root.right = TreeNode(0)
        
        serialized = serialize(root)
        assert serialized == "0,0,0"
        
        deserialized = deserialize(serialized)
        assert deserialized.val == 0
        assert deserialized.left.val == 0
        assert deserialized.right.val == 0
