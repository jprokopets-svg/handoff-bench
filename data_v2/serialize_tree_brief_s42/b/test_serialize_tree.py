import pytest
from serialize_tree import TreeNode, serialize, deserialize


class TestSerializeTree:
    """Test cases for binary tree serialization and deserialization."""
    
    def test_empty_tree(self):
        """Test serialization of an empty tree."""
        assert serialize(None) == ""
    
    def test_single_node(self):
        """Test serialization of a single node tree."""
        root = TreeNode(1)
        serialized = serialize(root)
        assert serialized == "1"
        deserialized = deserialize(serialized)
        assert deserialized.val == 1
        assert deserialized.left is None
        assert deserialized.right is None
    
    def test_balanced_tree(self):
        """Test serialization of a balanced tree."""
        #       1
        #      / \
        #     2   3
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        
        serialized = serialize(root)
        assert serialized == "1,2,3"
        
        deserialized = deserialize(serialized)
        assert deserialized.val == 1
        assert deserialized.left.val == 2
        assert deserialized.right.val == 3
    
    def test_left_skewed_tree(self):
        """Test serialization of a left-skewed tree."""
        #       1
        #      /
        #     2
        #    /
        #   3
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
        """Test serialization of a right-skewed tree."""
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
    
    def test_complex_tree(self):
        """Test serialization of a more complex tree."""
        #         1
        #        / \
        #       2   3
        #      / \
        #     4   5
        #        /
        #       6
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        root.left.left = TreeNode(4)
        root.left.right = TreeNode(5)
        root.left.right.left = TreeNode(6)
        
        serialized = serialize(root)
        deserialized = deserialize(serialized)
        
        # Verify structure
        assert deserialized.val == 1
        assert deserialized.left.val == 2
        assert deserialized.right.val == 3
        assert deserialized.left.left.val == 4
        assert deserialized.left.right.val == 5
        assert deserialized.left.right.left.val == 6
        assert deserialized.left.right.right is None
    
    def test_null_in_middle(self):
        """Test tree with null nodes in the middle (not just trailing)."""
        #       1
        #      / \
        #     2   3
        #      \
        #       4
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        root.left.right = TreeNode(4)
        
        serialized = serialize(root)
        deserialized = deserialize(serialized)
        
        assert deserialized.val == 1
        assert deserialized.left.val == 2
        assert deserialized.right.val == 3
        assert deserialized.left.left is None
        assert deserialized.left.right.val == 4
    
    def test_round_trip(self):
        """Test that serialize -> deserialize -> serialize produces the same result."""
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        root.left.left = TreeNode(4)
        root.left.right = TreeNode(5)
        
        serialized1 = serialize(root)
        deserialized = deserialize(serialized1)
        serialized2 = serialize(deserialized)
        
        assert serialized1 == serialized2
    
    def test_deserialize_empty_string(self):
        """Test deserialization of an empty string."""
        assert deserialize("") is None
    
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
