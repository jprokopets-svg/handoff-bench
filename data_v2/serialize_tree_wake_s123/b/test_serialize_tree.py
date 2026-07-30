"""
Test cases for binary tree serialization and deserialization.
"""

import pytest
from serialize_tree import TreeNode, serialize, deserialize


class TestSerialize:
    """Test serialization of binary trees."""
    
    def test_serialize_empty_tree(self):
        """Empty tree should serialize to empty string."""
        assert serialize(None) == ""
    
    def test_serialize_single_node(self):
        """Single node tree should serialize to just the value."""
        root = TreeNode(1)
        assert serialize(root) == "1"
    
    def test_serialize_complete_tree(self):
        """Complete binary tree should serialize correctly."""
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
    
    def test_serialize_tree_with_nulls_in_middle(self):
        """Tree with null nodes in the middle."""
        #       1
        #      / \
        #    null 2
        root = TreeNode(1)
        root.right = TreeNode(2)
        
        assert serialize(root) == "1,null,2"
    
    def test_serialize_left_skewed_tree(self):
        """Left-skewed tree."""
        #       1
        #      /
        #     2
        #    /
        #   3
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.left.left = TreeNode(3)
        
        assert serialize(root) == "1,2,null,3"
    
    def test_serialize_right_skewed_tree(self):
        """Right-skewed tree."""
        #     1
        #      \
        #       2
        #        \
        #         3
        root = TreeNode(1)
        root.right = TreeNode(2)
        root.right.right = TreeNode(3)
        
        assert serialize(root) == "1,null,2,null,3"


class TestDeserialize:
    """Test deserialization of binary trees."""
    
    def test_deserialize_empty_string(self):
        """Empty string should deserialize to None."""
        assert deserialize("") is None
    
    def test_deserialize_single_node(self):
        """Single node string should deserialize correctly."""
        root = deserialize("1")
        assert root.val == 1
        assert root.left is None
        assert root.right is None
    
    def test_deserialize_complete_tree(self):
        """Complete binary tree should deserialize correctly."""
        root = deserialize("1,2,3,4,5,6,7")
        
        assert root.val == 1
        assert root.left.val == 2
        assert root.right.val == 3
        assert root.left.left.val == 4
        assert root.left.right.val == 5
        assert root.right.left.val == 6
        assert root.right.right.val == 7
    
    def test_deserialize_tree_with_nulls_in_middle(self):
        """Tree with null nodes in the middle."""
        root = deserialize("1,null,2")
        
        assert root.val == 1
        assert root.left is None
        assert root.right.val == 2
    
    def test_deserialize_left_skewed_tree(self):
        """Left-skewed tree."""
        root = deserialize("1,2,null,3")
        
        assert root.val == 1
        assert root.left.val == 2
        assert root.right is None
        assert root.left.left.val == 3
        assert root.left.right is None
    
    def test_deserialize_right_skewed_tree(self):
        """Right-skewed tree."""
        root = deserialize("1,null,2,null,3")
        
        assert root.val == 1
        assert root.left is None
        assert root.right.val == 2
        assert root.right.left is None
        assert root.right.right.val == 3


class TestRoundTrip:
    """Test serialization and deserialization round trips."""
    
    def _tree_equal(self, node1, node2):
        """Check if two trees are structurally equal."""
        if node1 is None and node2 is None:
            return True
        if node1 is None or node2 is None:
            return False
        return (node1.val == node2.val and 
                self._tree_equal(node1.left, node2.left) and
                self._tree_equal(node1.right, node2.right))
    
    def test_roundtrip_empty_tree(self):
        """Empty tree should survive round trip."""
        original = None
        serialized = serialize(original)
        deserialized = deserialize(serialized)
        assert self._tree_equal(original, deserialized)
    
    def test_roundtrip_single_node(self):
        """Single node should survive round trip."""
        original = TreeNode(1)
        serialized = serialize(original)
        deserialized = deserialize(serialized)
        assert self._tree_equal(original, deserialized)
    
    def test_roundtrip_complete_tree(self):
        """Complete tree should survive round trip."""
        original = TreeNode(1)
        original.left = TreeNode(2)
        original.right = TreeNode(3)
        original.left.left = TreeNode(4)
        original.left.right = TreeNode(5)
        original.right.left = TreeNode(6)
        original.right.right = TreeNode(7)
        
        serialized = serialize(original)
        deserialized = deserialize(serialized)
        assert self._tree_equal(original, deserialized)
    
    def test_roundtrip_tree_with_nulls(self):
        """Tree with nulls should survive round trip."""
        original = TreeNode(1)
        original.right = TreeNode(2)
        original.right.right = TreeNode(3)
        
        serialized = serialize(original)
        deserialized = deserialize(serialized)
        assert self._tree_equal(original, deserialized)
    
    def test_roundtrip_complex_tree(self):
        """Complex tree with various null patterns."""
        original = TreeNode(1)
        original.left = TreeNode(2)
        original.right = TreeNode(3)
        original.left.right = TreeNode(4)
        original.right.left = TreeNode(5)
        
        serialized = serialize(original)
        deserialized = deserialize(serialized)
        assert self._tree_equal(original, deserialized)
