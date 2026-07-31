"""
Test suite for maximum path sum in binary tree.
"""

import pytest
from max_path_sum import TreeNode, maxPathSum


class TestMaxPathSum:
    """Test cases for maxPathSum function."""
    
    def test_single_node(self):
        """Test with a single node."""
        root = TreeNode(5)
        assert maxPathSum(root) == 5
    
    def test_single_node_negative(self):
        """Test with a single negative node."""
        root = TreeNode(-3)
        assert maxPathSum(root) == -3
    
    def test_two_nodes_positive(self):
        """Test with two positive nodes."""
        root = TreeNode(1)
        root.left = TreeNode(2)
        assert maxPathSum(root) == 3
    
    def test_two_nodes_negative(self):
        """Test with two nodes, one negative."""
        root = TreeNode(1)
        root.left = TreeNode(-2)
        assert maxPathSum(root) == 1
    
    def test_simple_tree(self):
        """Test with a simple balanced tree."""
        #       1
        #      / \
        #     2   3
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        assert maxPathSum(root) == 6
    
    def test_tree_with_negative_values(self):
        """Test with mixed positive and negative values."""
        #       -10
        #       /  \
        #      9    20
        #         /  \
        #        15   7
        root = TreeNode(-10)
        root.left = TreeNode(9)
        root.right = TreeNode(20)
        root.right.left = TreeNode(15)
        root.right.right = TreeNode(7)
        # Maximum path: 15 + 20 + 7 = 42
        assert maxPathSum(root) == 42
    
    def test_all_negative_values(self):
        """Test with all negative values."""
        #       -2
        #      /  \
        #    -1   -3
        root = TreeNode(-2)
        root.left = TreeNode(-1)
        root.right = TreeNode(-3)
        # Maximum path: -1 (single node)
        assert maxPathSum(root) == -1
    
    def test_path_through_root(self):
        """Test where maximum path goes through root."""
        #       10
        #      /  \
        #     5    15
        root = TreeNode(10)
        root.left = TreeNode(5)
        root.right = TreeNode(15)
        assert maxPathSum(root) == 30
    
    def test_path_not_through_root(self):
        """Test where maximum path doesn't go through root."""
        #       1
        #      / \
        #     2   3
        #    /
        #   4
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        root.left.left = TreeNode(4)
        # Maximum path: 4 + 2 = 6
        assert maxPathSum(root) == 6
    
    def test_deep_tree(self):
        """Test with a deeper tree."""
        #         1
        #        /
        #       2
        #      /
        #     3
        #    /
        #   4
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.left.left = TreeNode(3)
        root.left.left.left = TreeNode(4)
        assert maxPathSum(root) == 10
    
    def test_right_skewed_tree(self):
        """Test with a right-skewed tree."""
        #     1
        #      \
        #       2
        #        \
        #         3
        root = TreeNode(1)
        root.right = TreeNode(2)
        root.right.right = TreeNode(3)
        assert maxPathSum(root) == 6
    
    def test_complex_tree(self):
        """Test with a more complex tree."""
        #           5
        #          / \
        #         4   8
        #        /   / \
        #       11  13  4
        #      / \      \
        #     7   2      1
        root = TreeNode(5)
        root.left = TreeNode(4)
        root.right = TreeNode(8)
        root.left.left = TreeNode(11)
        root.left.left.left = TreeNode(7)
        root.left.left.right = TreeNode(2)
        root.right.left = TreeNode(13)
        root.right.right = TreeNode(4)
        root.right.right.right = TreeNode(1)
        # Maximum path: 7 + 11 + 4 + 5 + 8 + 13 = 48
        assert maxPathSum(root) == 48
    
    def test_empty_tree(self):
        """Test with an empty tree (None root)."""
        assert maxPathSum(None) == 0
    
    def test_single_large_value(self):
        """Test with a single large value."""
        root = TreeNode(1000)
        assert maxPathSum(root) == 1000
    
    def test_large_negative_value(self):
        """Test with a single large negative value."""
        root = TreeNode(-1000)
        assert maxPathSum(root) == -1000
