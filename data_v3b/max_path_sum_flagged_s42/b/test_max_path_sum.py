"""
Test cases for maximum path sum in binary tree.
"""

import pytest
from max_path_sum import TreeNode, maxPathSum


class TestMaxPathSum:
    """Test suite for maxPathSum function."""
    
    def test_single_node(self):
        """Test with a single node."""
        root = TreeNode(5)
        assert maxPathSum(root) == 5
    
    def test_single_negative_node(self):
        """Test with a single negative node."""
        root = TreeNode(-5)
        assert maxPathSum(root) == -5
    
    def test_empty_tree(self):
        """Test with empty tree (None)."""
        assert maxPathSum(None) == 0
    
    def test_two_nodes_positive(self):
        """Test with two positive nodes."""
        root = TreeNode(1)
        root.left = TreeNode(2)
        assert maxPathSum(root) == 3
    
    def test_two_nodes_negative(self):
        """Test with two negative nodes."""
        root = TreeNode(-1)
        root.left = TreeNode(-2)
        assert maxPathSum(root) == -1
    
    def test_simple_tree(self):
        """Test with a simple tree:
               1
              / \
             2   3
        """
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        assert maxPathSum(root) == 6
    
    def test_tree_with_negative_values(self):
        """Test with mixed positive and negative values:
               -10
              /   \
             9    20
                 /  \
                15   7
        """
        root = TreeNode(-10)
        root.left = TreeNode(9)
        root.right = TreeNode(20)
        root.right.left = TreeNode(15)
        root.right.right = TreeNode(7)
        # Maximum path is 15 + 20 + 7 = 42
        assert maxPathSum(root) == 42
    
    def test_all_negative_values(self):
        """Test with all negative values:
               -2
              /  \
            -1   -3
        """
        root = TreeNode(-2)
        root.left = TreeNode(-1)
        root.right = TreeNode(-3)
        # Maximum path is just -1 (single node)
        assert maxPathSum(root) == -1
    
    def test_path_through_root(self):
        """Test where maximum path goes through root:
               10
              /  \
             5    5
        """
        root = TreeNode(10)
        root.left = TreeNode(5)
        root.right = TreeNode(5)
        assert maxPathSum(root) == 20
    
    def test_path_not_through_root(self):
        """Test where maximum path doesn't go through root:
                 -1
                /  \
               2    3
              /
             4
        """
        root = TreeNode(-1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        root.left.left = TreeNode(4)
        # Maximum path is 4 + 2 = 6 (doesn't include root)
        assert maxPathSum(root) == 6
    
    def test_linear_tree_positive(self):
        """Test with linear tree (all left children):
             1
            /
           2
          /
         3
        """
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.left.left = TreeNode(3)
        assert maxPathSum(root) == 6
    
    def test_linear_tree_negative(self):
        """Test with linear tree with negative values:
             -1
            /
           -2
          /
         -3
        """
        root = TreeNode(-1)
        root.left = TreeNode(-2)
        root.left.left = TreeNode(-3)
        # Maximum is just -1 (single node)
        assert maxPathSum(root) == -1
    
    def test_complex_tree(self):
        """Test with a more complex tree:
                 1
               /   \
              2     3
             / \
            4   5
        """
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        root.left.left = TreeNode(4)
        root.left.right = TreeNode(5)
        # Maximum path is 4 + 2 + 1 + 3 = 10
        assert maxPathSum(root) == 10
    
    def test_large_positive_values(self):
        """Test with large positive values."""
        root = TreeNode(1000)
        root.left = TreeNode(2000)
        root.right = TreeNode(3000)
        assert maxPathSum(root) == 6000
    
    def test_single_right_child(self):
        """Test with only right child:
             1
              \
               2
        """
        root = TreeNode(1)
        root.right = TreeNode(2)
        assert maxPathSum(root) == 3
