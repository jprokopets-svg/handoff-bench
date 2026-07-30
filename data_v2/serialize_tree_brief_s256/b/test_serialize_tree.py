import pytest
from serialize_tree import TreeNode, serialize, deserialize


class TestSerializeTree:
    """Test suite for binary tree serialization and deserialization."""
    
    def test_empty_tree(self):
        """Test serialization of an empty tree."""
        result = serialize(None)
        assert result == ""
        
    def test_deserialize_empty_tree(self):
        """Test deserialization of an empty tree."""
        result = deserialize("")
        assert result is None
    
    def test_single_node(self):
        """Test serialization and deserialization of a single node."""
        root = TreeNode(1)
        serialized = serialize(root)
        assert serialized == "1"
        
        deserialized = deserialize(serialized)
        assert deserialized.val == 1
        assert deserialized.left is None
        assert deserialized.right is None
    
    def test_complete_binary_tree(self):
        """Test a complete binary tree."""
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
        deserialized = deserialize(serialized)
        
        # Verify structure
        assert deserialized.val == 1
        assert deserialized.left.val == 2
        assert deserialized.right.val == 3
        assert deserialized.left.left.val == 4
        assert deserialized.left.right.val == 5
        assert deserialized.right.left is None
        assert deserialized.right.right is None
    
    def test_left_skewed_tree(self):
        """Test a left-skewed tree."""
        #     1
        #    /
        #   2
        #  /
        # 3
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.left.left = TreeNode(3)
        
        serialized = serialize(root)
        deserialized = deserialize(serialized)
        
        assert deserialized.val == 1
        assert deserialized.left.val == 2
        assert deserialized.left.left.val == 3
        assert deserialized.right is None
        assert deserialized.left.right is None
    
    def test_right_skewed_tree(self):
        """Test a right-skewed tree."""
        #   1
        #    \
        #     2
        #      \
        #       3
        root = TreeNode(1)
        root.right = TreeNode(2)
        root.right.right = TreeNode(3)
        
        serialized = serialize(root)
        deserialized = deserialize(serialized)
        
        assert deserialized.val == 1
        assert deserialized.right.val == 2
        assert deserialized.right.right.val == 3
        assert deserialized.left is None
        assert deserialized.right.left is None
    
    def test_round_trip_serialization(self):
        """Test that serialize -> deserialize -> serialize produces identical output."""
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        root.left.left = TreeNode(4)
        root.right.right = TreeNode(5)
        
        serialized1 = serialize(root)
        deserialized = deserialize(serialized1)
        serialized2 = serialize(deserialized)
        
        assert serialized1 == serialized2
    
    def test_tree_with_gaps(self):
        """Test a tree with gaps (missing intermediate nodes)."""
        #       1
        #      / \
        #     2   3
        #        /
        #       4
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        root.right.left = TreeNode(4)
        
        serialized = serialize(root)
        deserialized = deserialize(serialized)
        
        assert deserialized.val == 1
        assert deserialized.left.val == 2
        assert deserialized.right.val == 3
        assert deserialized.right.left.val == 4
        assert deserialized.left.left is None
        assert deserialized.left.right is None
        assert deserialized.right.right is None
    
    def test_negative_values(self):
        """Test tree with negative node values."""
        root = TreeNode(-1)
        root.left = TreeNode(-2)
        root.right = TreeNode(3)
        
        serialized = serialize(root)
        deserialized = deserialize(serialized)
        
        assert deserialized.val == -1
        assert deserialized.left.val == -2
        assert deserialized.right.val == 3
    
    def test_large_values(self):
        """Test tree with large node values."""
        root = TreeNode(1000000)
        root.left = TreeNode(999999)
        root.right = TreeNode(1000001)
        
        serialized = serialize(root)
        deserialized = deserialize(serialized)
        
        assert deserialized.val == 1000000
        assert deserialized.left.val == 999999
        assert deserialized.right.val == 1000001
    
    def test_complex_tree(self):
        """Test a more complex tree structure."""
        #           1
        #         /   \
        #        2     3
        #       / \   / \
        #      4   5 6   7
        #     /         \
        #    8           9
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        root.left.left = TreeNode(4)
        root.left.right = TreeNode(5)
        root.right.left = TreeNode(6)
        root.right.right = TreeNode(7)
        root.left.left.left = TreeNode(8)
        root.right.right.right = TreeNode(9)
        
        serialized = serialize(root)
        deserialized = deserialize(serialized)
        
        # Verify all nodes
        assert deserialized.val == 1
        assert deserialized.left.val == 2
        assert deserialized.right.val == 3
        assert deserialized.left.left.val == 4
        assert deserialized.left.right.val == 5
        assert deserialized.right.left.val == 6
        assert deserialized.right.right.val == 7
        assert deserialized.left.left.left.val == 8
        assert deserialized.right.right.right.val == 9
        
        # Verify nulls
        assert deserialized.left.left.right is None
        assert deserialized.left.right.left is None
        assert deserialized.right.left.left is None
