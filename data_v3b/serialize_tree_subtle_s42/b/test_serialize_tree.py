"""
Test cases for binary tree serialization and deserialization.
"""

import pytest
from serialize_tree import TreeNode, serialize, deserialize


def trees_equal(node1, node2):
    """Helper function to compare two binary trees."""
    if node1 is None and node2 is None:
        return True
    if node1 is None or node2 is None:
        return False
    return (node1.val == node2.val and 
            trees_equal(node1.left, node2.left) and 
            trees_equal(node1.right, node2.right))


class TestSerialize:
    """Tests for the serialize function."""
    
    def test_empty_tree(self):
        """Test serializing an empty tree."""
        assert serialize(None) == ""
    
    def test_single_node(self):
        """Test serializing a tree with a single node."""
        root = TreeNode(1)
        assert serialize(root) == "1"
    
    def test_complete_binary_tree(self):
        """Test serializing a complete binary tree."""
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
        
        assert serialize(root) == "1,2,3,4,5,6,7"
    
    def test_tree_with_null_gaps(self):
        """Test serializing a tree with null gaps."""
        #     1
        #      \
        #       2
        root = TreeNode(1)
        root.right = TreeNode(2)
        
        assert serialize(root) == "1,null,2"
    
    def test_left_skewed_tree(self):
        """Test serializing a left-skewed tree."""
        #     1
        #    /
        #   2
        #  /
        # 3
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.left.left = TreeNode(3)
        
        assert serialize(root) == "1,2,null,3"
    
    def test_right_skewed_tree(self):
        """Test serializing a right-skewed tree."""
        #   1
        #    \
        #     2
        #      \
        #       3
        root = TreeNode(1)
        root.right = TreeNode(2)
        root.right.right = TreeNode(3)
        
        assert serialize(root) == "1,null,2,null,3"


class TestDeserialize:
    """Tests for the deserialize function."""
    
    def test_empty_string(self):
        """Test deserializing an empty string."""
        assert deserialize("") is None
    
    def test_single_node(self):
        """Test deserializing a single node."""
        root = deserialize("1")
        assert root.val == 1
        assert root.left is None
        assert root.right is None
    
    def test_complete_binary_tree(self):
        """Test deserializing a complete binary tree."""
        root = deserialize("1,2,3,4,5,6,7")
        
        assert root.val == 1
        assert root.left.val == 2
        assert root.right.val == 3
        assert root.left.left.val == 4
        assert root.left.right.val == 5
        assert root.right.left.val == 6
        assert root.right.right.val == 7
    
    def test_tree_with_null_gaps(self):
        """Test deserializing a tree with null gaps."""
        root = deserialize("1,null,2")
        
        assert root.val == 1
        assert root.left is None
        assert root.right.val == 2
    
    def test_left_skewed_tree(self):
        """Test deserializing a left-skewed tree."""
        root = deserialize("1,2,null,3")
        
        assert root.val == 1
        assert root.left.val == 2
        assert root.right is None
        assert root.left.left.val == 3
    
    def test_right_skewed_tree(self):
        """Test deserializing a right-skewed tree."""
        root = deserialize("1,null,2,null,3")
        
        assert root.val == 1
        assert root.left is None
        assert root.right.val == 2
        assert root.right.right.val == 3


class TestRoundTrip:
    """Tests for round-trip serialization and deserialization."""
    
    def test_round_trip_empty_tree(self):
        """Test round-trip with empty tree."""
        original = None
        serialized = serialize(original)
        deserialized = deserialize(serialized)
        assert trees_equal(original, deserialized)
    
    def test_round_trip_single_node(self):
        """Test round-trip with single node."""
        original = TreeNode(1)
        serialized = serialize(original)
        deserialized = deserialize(serialized)
        assert trees_equal(original, deserialized)
    
    def test_round_trip_complete_tree(self):
        """Test round-trip with complete binary tree."""
        original = TreeNode(1)
        original.left = TreeNode(2)
        original.right = TreeNode(3)
        original.left.left = TreeNode(4)
        original.left.right = TreeNode(5)
        original.right.left = TreeNode(6)
        original.right.right = TreeNode(7)
        
        serialized = serialize(original)
        deserialized = deserialize(serialized)
        assert trees_equal(original, deserialized)
    
    def test_round_trip_with_null_gaps(self):
        """Test round-trip with null gaps."""
        original = TreeNode(1)
        original.right = TreeNode(2)
        
        serialized = serialize(original)
        deserialized = deserialize(serialized)
        assert trees_equal(original, deserialized)
    
    def test_round_trip_complex_tree(self):
        """Test round-trip with complex tree structure."""
        #       1
        #      / \
        #     2   3
        #    /     \
        #   4       5
        original = TreeNode(1)
        original.left = TreeNode(2)
        original.right = TreeNode(3)
        original.left.left = TreeNode(4)
        original.right.right = TreeNode(5)
        
        serialized = serialize(original)
        deserialized = deserialize(serialized)
        assert trees_equal(original, deserialized)
    
    def test_round_trip_negative_values(self):
        """Test round-trip with negative node values."""
        original = TreeNode(-1)
        original.left = TreeNode(-2)
        original.right = TreeNode(3)
        
        serialized = serialize(original)
        deserialized = deserialize(serialized)
        assert trees_equal(original, deserialized)
