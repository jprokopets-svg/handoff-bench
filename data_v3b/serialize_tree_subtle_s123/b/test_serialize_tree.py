import pytest
from serialize_tree import TreeNode, serialize, deserialize


def trees_equal(node1, node2):
    """Helper function to compare two trees for equality."""
    if node1 is None and node2 is None:
        return True
    if node1 is None or node2 is None:
        return False
    return (node1.val == node2.val and 
            trees_equal(node1.left, node2.left) and 
            trees_equal(node1.right, node2.right))


class TestSerializeDeserialize:
    
    def test_empty_tree(self):
        """Test serialization and deserialization of empty tree."""
        root = None
        serialized = serialize(root)
        assert serialized == ""
        deserialized = deserialize(serialized)
        assert deserialized is None
    
    def test_single_node(self):
        """Test serialization and deserialization of single node tree."""
        root = TreeNode(1)
        serialized = serialize(root)
        assert serialized == "1"
        deserialized = deserialize(serialized)
        assert trees_equal(root, deserialized)
    
    def test_complete_binary_tree(self):
        """Test serialization and deserialization of complete binary tree."""
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
        assert trees_equal(root, deserialized)
    
    def test_tree_with_nulls(self):
        """Test serialization and deserialization of tree with missing nodes."""
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
        deserialized = deserialize(serialized)
        assert trees_equal(root, deserialized)
    
    def test_left_skewed_tree(self):
        """Test serialization and deserialization of left-skewed tree."""
        #       1
        #      /
        #     2
        #    /
        #   3
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.left.left = TreeNode(3)
        
        serialized = serialize(root)
        deserialized = deserialize(serialized)
        assert trees_equal(root, deserialized)
    
    def test_right_skewed_tree(self):
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
        deserialized = deserialize(serialized)
        assert trees_equal(root, deserialized)
    
    def test_round_trip_consistency(self):
        """Test that serialize -> deserialize -> serialize produces same output."""
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        root.left.left = TreeNode(4)
        root.right.right = TreeNode(5)
        
        serialized1 = serialize(root)
        deserialized = deserialize(serialized1)
        serialized2 = serialize(deserialized)
        assert serialized1 == serialized2
    
    def test_tree_with_negative_values(self):
        """Test serialization and deserialization of tree with negative values."""
        root = TreeNode(-1)
        root.left = TreeNode(-2)
        root.right = TreeNode(3)
        root.left.left = TreeNode(-4)
        
        serialized = serialize(root)
        deserialized = deserialize(serialized)
        assert trees_equal(root, deserialized)
    
    def test_tree_with_duplicate_values(self):
        """Test serialization and deserialization of tree with duplicate values."""
        root = TreeNode(1)
        root.left = TreeNode(1)
        root.right = TreeNode(1)
        root.left.left = TreeNode(1)
        
        serialized = serialize(root)
        deserialized = deserialize(serialized)
        assert trees_equal(root, deserialized)
    
    def test_complex_tree(self):
        """Test serialization and deserialization of complex tree."""
        #           1
        #         /   \
        #        2     3
        #       / \   /
        #      4   5 6
        #     /
        #    7
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        root.left.left = TreeNode(4)
        root.left.right = TreeNode(5)
        root.right.left = TreeNode(6)
        root.left.left.left = TreeNode(7)
        
        serialized = serialize(root)
        deserialized = deserialize(serialized)
        assert trees_equal(root, deserialized)
