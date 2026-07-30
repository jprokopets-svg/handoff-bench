import pytest
from serialize_tree import TreeNode, serialize, deserialize


class TestSerializeTree:
    """Test cases for binary tree serialization and deserialization."""
    
    def test_empty_tree(self):
        """Test serializing and deserializing an empty tree."""
        root = None
        serialized = serialize(root)
        assert serialized == ""
        deserialized = deserialize(serialized)
        assert deserialized is None
    
    def test_single_node(self):
        """Test serializing and deserializing a single node."""
        root = TreeNode(1)
        serialized = serialize(root)
        assert serialized == "1"
        deserialized = deserialize(serialized)
        assert deserialized.val == 1
        assert deserialized.left is None
        assert deserialized.right is None
    
    def test_complete_tree_three_nodes(self):
        """Test serializing and deserializing a complete tree with 3 nodes."""
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
    
    def test_tree_with_nulls_in_middle(self):
        """Test serializing and deserializing a tree with null nodes in the middle."""
        #     1
        #    / \
        #   2   null
        #  /
        # 4
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.left.left = TreeNode(4)
        
        serialized = serialize(root)
        assert serialized == "1,2,null,4"
        
        deserialized = deserialize(serialized)
        assert deserialized.val == 1
        assert deserialized.left.val == 2
        assert deserialized.right is None
        assert deserialized.left.left.val == 4
        assert deserialized.left.right is None
    
    def test_tree_with_right_child_only(self):
        """Test serializing and deserializing a tree with only right children."""
        #     1
        #      \
        #       2
        #        \
        #         3
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
    
    def test_round_trip_serialization(self):
        """Test that serialize -> deserialize -> serialize produces the same result."""
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
        
        serialized1 = serialize(root)
        deserialized = deserialize(serialized1)
        serialized2 = serialize(deserialized)
        
        assert serialized1 == serialized2
    
    def test_complex_tree_with_multiple_nulls(self):
        """Test a more complex tree structure."""
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
    
    def test_single_left_child(self):
        """Test a tree with only a left child at root."""
        #   1
        #  /
        # 2
        root = TreeNode(1)
        root.left = TreeNode(2)
        
        serialized = serialize(root)
        assert serialized == "1,2"
        
        deserialized = deserialize(serialized)
        assert deserialized.val == 1
        assert deserialized.left.val == 2
        assert deserialized.right is None
    
    def test_single_right_child(self):
        """Test a tree with only a right child at root."""
        #   1
        #    \
        #     2
        root = TreeNode(1)
        root.right = TreeNode(2)
        
        serialized = serialize(root)
        assert serialized == "1,null,2"
        
        deserialized = deserialize(serialized)
        assert deserialized.val == 1
        assert deserialized.left is None
        assert deserialized.right.val == 2
