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


def test_path_not_through_root():
    """Test where max path doesn't go through root"""
    root = TreeNode(-10)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    # Max path is 15 + 20 + 7 = 42
    assert maxPathSum(root) == 42


def test_all_negative():
    """Test where all values are negative"""
    root = TreeNode(-2)
    root.left = TreeNode(-1)
    assert maxPathSum(root) == -1


def test_complex_tree():
    """Test with a more complex tree"""
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    # Max path could be 4 + 2 + 1 + 3 = 10 or 5 + 2 + 1 + 3 = 11
    assert maxPathSum(root) == 11


def test_empty_tree():
    """Test with None root"""
    assert maxPathSum(None) == 0
