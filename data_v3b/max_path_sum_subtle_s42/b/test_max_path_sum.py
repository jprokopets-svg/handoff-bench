"""
Test cases for the maximum path sum in a binary tree.
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
        """Test with an empty tree."""
        assert maxPathSum(None) == 0
    
    def test_simple_tree(self):
        """Test with a simple tree: 
               1
              / \
             2   3
        """
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        assert maxPathSum(root) == 6  # 2 + 1 + 3
    
    def test_tree_with_negative_values(self):
        """Test with a tree containing negative values:
               1
              / \
            -2   3
        """
        root = TreeNode(1)
        root.left = TreeNode(-2)
        root.right = TreeNode(3)
        assert maxPathSum(root) == 4  # 1 + 3 (ignore -2)
    
    def test_all_negative_values(self):
        """Test with all negative values:
              -1
              / \
            -2  -3
        """
        root = TreeNode(-1)
        root.left = TreeNode(-2)
        root.right = TreeNode(-3)
        assert maxPathSum(root) == -1  # Best single node
    
    def test_linear_tree_left(self):
        """Test with a linear tree (left only):
             1
            /
           2
          /
         3
        """
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.left.left = TreeNode(3)
        assert maxPathSum(root) == 6  # 3 + 2 + 1
    
    def test_linear_tree_right(self):
        """Test with a linear tree (right only):
             1
              \
               2
                \
                 3
        """
        root = TreeNode(1)
        root.right = TreeNode(2)
        root.right.right = TreeNode(3)
        assert maxPathSum(root) == 6  # 1 + 2 + 3
    
    def test_complex_tree(self):
        """Test with a more complex tree:
               -10
               /  \
              9   20
                 /  \
                15   7
        Expected: 15 + 20 + 7 = 42
        """
        root = TreeNode(-10)
        root.left = TreeNode(9)
        root.right = TreeNode(20)
        root.right.left = TreeNode(15)
        root.right.right = TreeNode(7)
        assert maxPathSum(root) == 42
    
    def test_path_not_through_root(self):
        """Test where the maximum path doesn't go through root:
               1
              / \
             2   3
            /
           4
        Maximum path: 4 + 2 = 6 (doesn't include root)
        """
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        root.left.left = TreeNode(4)
        assert maxPathSum(root) == 6
    
    def test_large_positive_values(self):
        """Test with large positive values."""
        root = TreeNode(1000)
        root.left = TreeNode(2000)
        root.right = TreeNode(3000)
        assert maxPathSum(root) == 6000
    
    def test_mixed_positive_negative(self):
        """Test with mixed positive and negative values:
                5
               / \
              4   8
             /   / \
            11  13  4
                   \
                    1
        """
        root = TreeNode(5)
        root.left = TreeNode(4)
        root.right = TreeNode(8)
        root.left.left = TreeNode(11)
        root.right.left = TreeNode(13)
        root.right.right = TreeNode(4)
        root.right.right.right = TreeNode(1)
        # Maximum path: 11 + 4 + 5 + 8 + 13 = 41
        assert maxPathSum(root) == 41
    
    def test_single_path_with_zeros(self):
        """Test with zeros in the tree:
             0
            / \
           0   0
        """
        root = TreeNode(0)
        root.left = TreeNode(0)
        root.right = TreeNode(0)
        assert maxPathSum(root) == 0
    
    def test_negative_root_positive_children(self):
        """Test with negative root and positive children:
              -5
              / \
             10  20
        """
        root = TreeNode(-5)
        root.left = TreeNode(10)
        root.right = TreeNode(20)
        assert maxPathSum(root) == 30  # 10 + (-5) + 20
