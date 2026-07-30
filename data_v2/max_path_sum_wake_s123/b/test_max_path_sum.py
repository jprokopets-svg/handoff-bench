"""
Test cases for maximum path sum in a binary tree.
"""

import pytest
from max_path_sum import TreeNode, maxPathSum


class TestMaxPathSum:
    """Test cases for the maxPathSum function."""
    
    def test_single_node(self):
        """Test with a single node."""
        root = TreeNode(1)
        assert maxPathSum(root) == 1
    
    def test_single_negative_node(self):
        """Test with a single negative node."""
        root = TreeNode(-3)
        assert maxPathSum(root) == -3
    
    def test_two_nodes_positive(self):
        """Test with two positive nodes."""
        root = TreeNode(1)
        root.left = TreeNode(2)
        assert maxPathSum(root) == 3
    
    def test_two_nodes_right(self):
        """Test with two nodes on the right."""
        root = TreeNode(1)
        root.right = TreeNode(2)
        assert maxPathSum(root) == 3
    
    def test_simple_tree(self):
        """Test with a simple tree."""
        #       1
        #      / \
        #     2   3
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        assert maxPathSum(root) == 6
    
    def test_tree_with_negative_values(self):
        """Test tree with negative values."""
        #       -10
        #       /  \
        #      9   20
        #         /  \
        #        15   7
        root = TreeNode(-10)
        root.left = TreeNode(9)
        root.right = TreeNode(20)
        root.right.left = TreeNode(15)
        root.right.right = TreeNode(7)
        # Path 15 -> 20 -> 7 = 42
        assert maxPathSum(root) == 42
    
    def test_all_negative_values(self):
        """Test tree with all negative values."""
        #       -3
        #      /  \
        #    -2   -1
        root = TreeNode(-3)
        root.left = TreeNode(-2)
        root.right = TreeNode(-1)
        # Best path is just the node -1
        assert maxPathSum(root) == -1
    
    def test_path_through_root(self):
        """Test path that goes through the root."""
        #       10
        #      /  \
        #     5   15
        root = TreeNode(10)
        root.left = TreeNode(5)
        root.right = TreeNode(15)
        assert maxPathSum(root) == 30
    
    def test_path_not_through_root(self):
        """Test path that doesn't go through the root."""
        #       1
        #      / \
        #     2   3
        #    /
        #   4
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        root.left.left = TreeNode(4)
        # Path 4 -> 2 -> 1 -> 3 = 10
        assert maxPathSum(root) == 10
    
    def test_single_long_path(self):
        """Test a tree where the best path is a single long branch."""
        #       1
        #        \
        #         2
        #          \
        #           3
        #            \
        #             4
        root = TreeNode(1)
        root.right = TreeNode(2)
        root.right.right = TreeNode(3)
        root.right.right.right = TreeNode(4)
        assert maxPathSum(root) == 10
    
    def test_negative_left_positive_right(self):
        """Test with negative left subtree and positive right."""
        #       5
        #      / \
        #    -5  10
        root = TreeNode(5)
        root.left = TreeNode(-5)
        root.right = TreeNode(10)
        # Best path is 5 + 10 = 15
        assert maxPathSum(root) == 15
    
    def test_complex_tree(self):
        """Test a more complex tree."""
        #         2
        #        / \
        #       1   3
        #      /
        #    -2
        root = TreeNode(2)
        root.left = TreeNode(1)
        root.right = TreeNode(3)
        root.left.left = TreeNode(-2)
        # Best path is 2 + 1 + 3 = 6 or just 2 + 3 = 5 or 1 + 2 + 3 = 6
        assert maxPathSum(root) == 6
    
    def test_single_node_zero(self):
        """Test with a single zero node."""
        root = TreeNode(0)
        assert maxPathSum(root) == 0
    
    def test_mixed_positive_negative(self):
        """Test with mixed positive and negative values."""
        #       -2
        #      /  \
        #     1   -3
        root = TreeNode(-2)
        root.left = TreeNode(1)
        root.right = TreeNode(-3)
        # Best path is just 1
        assert maxPathSum(root) == 1
