"""
Test cases for max_path_sum function
"""

import pytest
from max_path_sum import maxPathSum, TreeNode


def test_single_node():
    """Test with a single node"""
    root = TreeNode(5)
    assert maxPathSum(root) == 5


def test_two_nodes():
    """Test with two nodes"""
    root = TreeNode(1)
    root.left = TreeNode(2)
    assert maxPathSum(root) == 3


def test_negative_values():
    """Test with negative values"""
    root = TreeNode(-3)
    assert maxPathSum(root) == -3


def test_mixed_positive_negative():
    """Test with mixed positive and negative values"""
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    assert maxPathSum(root) == 6


def test_complex_tree():
    """Test with a more complex tree"""
    #       1
    #      / \
    #     2   3
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    assert maxPathSum(root) == 6


def test_negative_path():
    """Test where we need to skip negative branches"""
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
    assert maxPathSum(root) == 42


def test_all_negative():
    """Test with all negative values"""
    #      -2
    #      /
    #    -1
    root = TreeNode(-2)
    root.left = TreeNode(-1)
    assert maxPathSum(root) == -1


def test_large_positive_values():
    """Test with large positive values"""
    root = TreeNode(100)
    root.left = TreeNode(50)
    root.right = TreeNode(75)
    assert maxPathSum(root) == 225
