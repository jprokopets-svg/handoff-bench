"""
Test cases for maxPathSum function
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
        root = TreeNode(-5)
        assert maxPathSum(root) == -5
    
    def test_empty_tree(self):
        """Test with empty tree"""
        assert maxPathSum(None) == 0
    
    def test_two_nodes_positive(self):
        """Test with two positive nodes"""
        root = TreeNode(1)
        root.left = TreeNode(2)
        assert maxPathSum(root) == 3
    
    def test_two_nodes_right(self):
        """Test with two nodes on right"""
        root = TreeNode(1)
        root.right = TreeNode(2)
        assert maxPathSum(root) == 3
    
    def test_all_positive_values(self):
        """Test tree with all positive values"""
        #       10
        #      /  \
        #     5    15
        #    / \
        #   3   7
        root = TreeNode(10)
        root.left = TreeNode(5)
        root.right = TreeNode(15)
        root.left.left = TreeNode(3)
        root.left.right = TreeNode(7)
        # Max path: 3 + 5 + 10 + 15 = 33
        assert maxPathSum(root) == 33
    
    def test_with_negative_values(self):
        """Test tree with negative values"""
        #       -10
        #      /   \
        #     9     20
        #          /  \
        #         15   7
        root = TreeNode(-10)
        root.left = TreeNode(9)
        root.right = TreeNode(20)
        root.right.left = TreeNode(15)
        root.right.right = TreeNode(7)
        # Max path: 15 + 20 + 7 = 42
        assert maxPathSum(root) == 42
    
    def test_path_not_through_root(self):
        """Test where max path doesn't go through root"""
        #       1
        #      / \
        #    -2   3
        #    /
        #   4
        root = TreeNode(1)
        root.left = TreeNode(-2)
        root.right = TreeNode(3)
        root.left.left = TreeNode(4)
        # Max path: 4 + (-2) = 2, or just 3, or 1+3=4
        # Actually: 4 + (-2) + 1 + 3 = 6
        assert maxPathSum(root) == 6
    
    def test_all_negative_values(self):
        """Test tree with all negative values - should return least negative"""
        #       -1
        #      /  \
        #    -2   -3
        root = TreeNode(-1)
        root.left = TreeNode(-2)
        root.right = TreeNode(-3)
        # Max path: just -1
        assert maxPathSum(root) == -1
    
    def test_linear_tree_left(self):
        """Test linear tree going left"""
        #     1
        #    /
        #   2
        #  /
        # 3
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.left.left = TreeNode(3)
        assert maxPathSum(root) == 6
    
    def test_linear_tree_right(self):
        """Test linear tree going right"""
        #   1
        #    \
        #     2
        #      \
        #       3
        root = TreeNode(1)
        root.right = TreeNode(2)
        root.right.right = TreeNode(3)
        assert maxPathSum(root) == 6
    
    def test_complex_tree(self):
        """Test a more complex tree"""
        #         5
        #        / \
        #       4   8
        #      /   / \
        #     11  13  4
        #    / \      \
        #   7   2      1
        root = TreeNode(5)
        root.left = TreeNode(4)
        root.right = TreeNode(8)
        root.left.left = TreeNode(11)
        root.left.left.left = TreeNode(7)
        root.left.left.right = TreeNode(2)
        root.right.left = TreeNode(13)
        root.right.right = TreeNode(4)
        root.right.right.right = TreeNode(1)
        # Max path could be: 7 + 11 + 4 + 5 + 8 + 13 = 48
        assert maxPathSum(root) == 48
    
    def test_single_large_positive(self):
        """Test with single large positive value"""
        root = TreeNode(1000)
        assert maxPathSum(root) == 1000
    
    def test_mixed_positive_negative(self):
        """Test with mixed positive and negative"""
        #       10
        #      /  \
        #    -5   20
        #    / \
        #   3  -2
        root = TreeNode(10)
        root.left = TreeNode(-5)
        root.right = TreeNode(20)
        root.left.left = TreeNode(3)
        root.left.right = TreeNode(-2)
        # Max path: 3 + (-5) + 10 + 20 = 28
        assert maxPathSum(root) == 28
