"""
Test cases for maximum path sum in binary tree
"""

import pytest
from max_path_sum import TreeNode, maxPathSum


class TestMaxPathSum:
    """Test suite for maxPathSum function"""
    
    def test_single_node(self):
        """Test with a single node"""
        root = TreeNode(5)
        assert maxPathSum(root) == 5
    
    def test_single_negative_node(self):
        """Test with a single negative node"""
        root = TreeNode(-10)
        assert maxPathSum(root) == -10
    
    def test_two_nodes_positive(self):
        """Test with two positive nodes"""
        root = TreeNode(1)
        root.left = TreeNode(2)
        assert maxPathSum(root) == 3
    
    def test_two_nodes_negative(self):
        """Test with two nodes where child is negative"""
        root = TreeNode(1)
        root.left = TreeNode(-2)
        assert maxPathSum(root) == 1
    
    def test_simple_tree(self):
        """Test with simple tree [1,2,3]"""
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        assert maxPathSum(root) == 6
    
    def test_all_negative(self):
        """Test with all negative values"""
        root = TreeNode(-10)
        root.left = TreeNode(-5)
        root.right = TreeNode(-3)
        assert maxPathSum(root) == -3
    
    def test_mixed_positive_negative(self):
        """Test with mixed positive and negative values"""
        # Tree: [-3, 9, 20, null, null, 15, 7]
        root = TreeNode(-3)
        root.left = TreeNode(9)
        root.right = TreeNode(20)
        root.right.left = TreeNode(15)
        root.right.right = TreeNode(7)
        assert maxPathSum(root) == 42  # 15 + 20 + 7
    
    def test_path_through_root(self):
        """Test where max path goes through root"""
        root = TreeNode(10)
        root.left = TreeNode(5)
        root.right = TreeNode(15)
        assert maxPathSum(root) == 30
    
    def test_path_in_left_subtree(self):
        """Test where max path is entirely in left subtree"""
        root = TreeNode(1)
        root.left = TreeNode(10)
        root.left.left = TreeNode(5)
        root.left.right = TreeNode(8)
        root.right = TreeNode(-5)
        assert maxPathSum(root) == 23  # 5 + 10 + 8
    
    def test_path_in_right_subtree(self):
        """Test where max path is entirely in right subtree"""
        root = TreeNode(1)
        root.left = TreeNode(-5)
        root.right = TreeNode(10)
        root.right.left = TreeNode(5)
        root.right.right = TreeNode(8)
        assert maxPathSum(root) == 23  # 5 + 10 + 8
    
    def test_single_node_path(self):
        """Test where max path is just a single node"""
        root = TreeNode(100)
        root.left = TreeNode(-50)
        root.right = TreeNode(-50)
        assert maxPathSum(root) == 100
    
    def test_deep_tree(self):
        """Test with a deeper tree"""
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.left.left = TreeNode(3)
        root.left.left.left = TreeNode(4)
        assert maxPathSum(root) == 10  # 4 + 3 + 2 + 1
    
    def test_unbalanced_tree(self):
        """Test with unbalanced tree"""
        root = TreeNode(5)
        root.left = TreeNode(4)
        root.left.left = TreeNode(11)
        root.left.left.left = TreeNode(7)
        root.left.left.right = TreeNode(2)
        root.right = TreeNode(8)
        root.right.right = TreeNode(4)
        root.right.right.right = TreeNode(5)
        # Max path: 7 + 11 + 4 + 5 + 2 = 29 (through 11)
        # Or: 7 + 11 + 4 = 22
        # Or: 2 + 11 + 4 = 17
        # Or: 5 + 4 + 8 + 5 = 22
        # Max should be 7 + 11 + 2 = 20
        assert maxPathSum(root) == 20
    
    def test_large_positive_values(self):
        """Test with large positive values"""
        root = TreeNode(1000)
        root.left = TreeNode(2000)
        root.right = TreeNode(3000)
        assert maxPathSum(root) == 6000
    
    def test_large_negative_values(self):
        """Test with large negative values"""
        root = TreeNode(-1000)
        root.left = TreeNode(-2000)
        root.right = TreeNode(-3000)
        assert maxPathSum(root) == -1000
