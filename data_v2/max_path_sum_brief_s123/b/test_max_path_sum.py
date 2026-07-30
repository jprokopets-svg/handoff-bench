"""
Test cases for Maximum Path Sum in Binary Tree
"""

import pytest
from max_path_sum import TreeNode, maxPathSum


class TestMaxPathSum:
    """Test suite for maxPathSum function"""
    
    def test_single_node_positive(self):
        """Test with a single positive node"""
        root = TreeNode(5)
        assert maxPathSum(root) == 5
    
    def test_single_node_negative(self):
        """Test with a single negative node"""
        root = TreeNode(-5)
        assert maxPathSum(root) == -5
    
    def test_empty_tree(self):
        """Test with empty tree (None)"""
        assert maxPathSum(None) == 0
    
    def test_simple_tree_left_right(self):
        """Test simple tree with left and right children"""
        #       1
        #      / \
        #     2   3
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        assert maxPathSum(root) == 6  # 2 + 1 + 3
    
    def test_all_negative(self):
        """Test tree with all negative values"""
        #       -1
        #      /  \
        #    -2   -3
        root = TreeNode(-1)
        root.left = TreeNode(-2)
        root.right = TreeNode(-3)
        assert maxPathSum(root) == -1  # Best is just the root node
    
    def test_path_not_through_root(self):
        """Test where best path is in a subtree, not through root"""
        #       -10
        #       /
        #      5
        #     / \
        #    3   2
        root = TreeNode(-10)
        root.left = TreeNode(5)
        root.left.left = TreeNode(3)
        root.left.right = TreeNode(2)
        assert maxPathSum(root) == 10  # 3 + 5 + 2
    
    def test_linear_tree_positive(self):
        """Test linear tree with all positive values"""
        #     1
        #    /
        #   2
        #  /
        # 3
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.left.left = TreeNode(3)
        assert maxPathSum(root) == 6  # 3 + 2 + 1
    
    def test_linear_tree_mixed(self):
        """Test linear tree with mixed positive and negative"""
        #     10
        #    /
        #   -5
        #  /
        # 3
        root = TreeNode(10)
        root.left = TreeNode(-5)
        root.left.left = TreeNode(3)
        assert maxPathSum(root) == 10  # Just the root is best
    
    def test_complex_tree(self):
        """Test a more complex tree structure"""
        #        -3
        #       /  \
        #      9   20
        #         /  \
        #        15   7
        root = TreeNode(-3)
        root.left = TreeNode(9)
        root.right = TreeNode(20)
        root.right.left = TreeNode(15)
        root.right.right = TreeNode(7)
        assert maxPathSum(root) == 42  # 15 + 20 + 7
    
    def test_single_left_child(self):
        """Test tree with only left child"""
        #     5
        #    /
        #   3
        root = TreeNode(5)
        root.left = TreeNode(3)
        assert maxPathSum(root) == 8
    
    def test_single_right_child(self):
        """Test tree with only right child"""
        #     5
        #      \
        #       3
        root = TreeNode(5)
        root.right = TreeNode(3)
        assert maxPathSum(root) == 8
    
    def test_balanced_tree(self):
        """Test a balanced tree"""
        #        1
        #       / \
        #      2   3
        #     / \
        #    4   5
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        root.left.left = TreeNode(4)
        root.left.right = TreeNode(5)
        assert maxPathSum(root) == 15  # 4 + 2 + 5 + 1 + 3
    
    def test_negative_root_positive_children(self):
        """Test negative root with positive children"""
        #       -1
        #      /  \
        #     5    6
        root = TreeNode(-1)
        root.left = TreeNode(5)
        root.right = TreeNode(6)
        assert maxPathSum(root) == 10  # 5 + (-1) + 6
    
    def test_large_values(self):
        """Test with large values"""
        #       1000
        #       /   \
        #     500   600
        root = TreeNode(1000)
        root.left = TreeNode(500)
        root.right = TreeNode(600)
        assert maxPathSum(root) == 2100
