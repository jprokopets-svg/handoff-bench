import pytest
from serialize_tree import TreeNode, serialize, deserialize


class TestSerialize:
    """Test cases for the serialize function"""
    
    def test_empty_tree(self):
        """Test serializing an empty tree"""
        assert serialize(None) == ""
    
    def test_single_node(self):
        """Test serializing a tree with a single node"""
        root = TreeNode(1)
        assert serialize(root) == "1"
    
    def test_complete_binary_tree(self):
        """Test serializing a complete binary tree"""
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
        
        result = serialize(root)
        assert result == "1,2,3,4,5"
    
    def test_tree_with_nulls(self):
        """Test serializing a tree with missing nodes"""
        #       1
        #      / \
        #     2   null
        #    / \
        #   4   5
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.left.left = TreeNode(4)
        root.left.right = TreeNode(5)
        
        result = serialize(root)
        assert result == "1,2,null,4,5"
    
    def test_only_left_children(self):
        """Test serializing a tree with only left children"""
        #       1
        #      /
        #     2
        #    /
        #   3
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.left.left = TreeNode(3)
        
        result = serialize(root)
        assert result == "1,2,null,3"
    
    def test_only_right_children(self):
        """Test serializing a tree with only right children"""
        #       1
        #        \
        #         2
        #          \
        #           3
        root = TreeNode(1)
        root.right = TreeNode(2)
        root.right.right = TreeNode(3)
        
        result = serialize(root)
        assert result == "1,null,2,null,3"


class TestDeserialize:
    """Test cases for the deserialize function"""
    
    def test_empty_string(self):
        """Test deserializing an empty string"""
        assert deserialize("") is None
    
    def test_single_node(self):
        """Test deserializing a single node"""
        root = deserialize("1")
        assert root.val == 1
        assert root.left is None
        assert root.right is None
    
    def test_complete_binary_tree(self):
        """Test deserializing a complete binary tree"""
        root = deserialize("1,2,3,4,5")
        assert root.val == 1
        assert root.left.val == 2
        assert root.right.val == 3
        assert root.left.left.val == 4
        assert root.left.right.val == 5
        assert root.right.left is None
        assert root.right.right is None
    
    def test_tree_with_nulls(self):
        """Test deserializing a tree with null nodes"""
        root = deserialize("1,2,null,4,5")
        assert root.val == 1
        assert root.left.val == 2
        assert root.right is None
        assert root.left.left.val == 4
        assert root.left.right.val == 5
    
    def test_only_left_children(self):
        """Test deserializing a tree with only left children"""
        root = deserialize("1,2,null,3")
        assert root.val == 1
        assert root.left.val == 2
        assert root.right is None
        assert root.left.left.val == 3
        assert root.left.right is None
    
    def test_only_right_children(self):
        """Test deserializing a tree with only right children"""
        root = deserialize("1,null,2,null,3")
        assert root.val == 1
        assert root.left is None
        assert root.right.val == 2
        assert root.right.left is None
        assert root.right.right.val == 3


class TestRoundTrip:
    """Test cases for round-trip serialization and deserialization"""
    
    def test_round_trip_empty_tree(self):
        """Test round-trip with empty tree"""
        original = None
        serialized = serialize(original)
        deserialized = deserialize(serialized)
        assert deserialized is None
    
    def test_round_trip_single_node(self):
        """Test round-trip with single node"""
        original = TreeNode(1)
        serialized = serialize(original)
        deserialized = deserialize(serialized)
        assert deserialized.val == 1
        assert deserialized.left is None
        assert deserialized.right is None
    
    def test_round_trip_complete_tree(self):
        """Test round-trip with complete binary tree"""
        original = TreeNode(1)
        original.left = TreeNode(2)
        original.right = TreeNode(3)
        original.left.left = TreeNode(4)
        original.left.right = TreeNode(5)
        
        serialized = serialize(original)
        deserialized = deserialize(serialized)
        
        # Verify structure
        assert deserialized.val == 1
        assert deserialized.left.val == 2
        assert deserialized.right.val == 3
        assert deserialized.left.left.val == 4
        assert deserialized.left.right.val == 5
        
        # Verify round-trip
        assert serialize(deserialized) == serialized
    
    def test_round_trip_unbalanced_tree(self):
        """Test round-trip with unbalanced tree"""
        original = TreeNode(1)
        original.left = TreeNode(2)
        original.left.left = TreeNode(3)
        original.right = TreeNode(4)
        original.right.right = TreeNode(5)
        
        serialized = serialize(original)
        deserialized = deserialize(serialized)
        
        # Verify structure
        assert deserialized.val == 1
        assert deserialized.left.val == 2
        assert deserialized.left.left.val == 3
        assert deserialized.right.val == 4
        assert deserialized.right.right.val == 5
        
        # Verify round-trip
        assert serialize(deserialized) == serialized
    
    def test_round_trip_complex_tree(self):
        """Test round-trip with a more complex tree"""
        #           1
        #         /   \
        #        2     3
        #       / \   /
        #      4   5 6
        #     /
        #    7
        original = TreeNode(1)
        original.left = TreeNode(2)
        original.right = TreeNode(3)
        original.left.left = TreeNode(4)
        original.left.right = TreeNode(5)
        original.right.left = TreeNode(6)
        original.left.left.left = TreeNode(7)
        
        serialized = serialize(original)
        deserialized = deserialize(serialized)
        
        # Verify structure
        assert deserialized.val == 1
        assert deserialized.left.val == 2
        assert deserialized.right.val == 3
        assert deserialized.left.left.val == 4
        assert deserialized.left.right.val == 5
        assert deserialized.right.left.val == 6
        assert deserialized.left.left.left.val == 7
        
        # Verify round-trip
        assert serialize(deserialized) == serialized
