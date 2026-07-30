import pytest
from max_path_sum import TreeNode, maxPathSum


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


def test_all_negative():
    """Test with all negative values"""
    root = TreeNode(-2)
    root.left = TreeNode(-1)
    root.right = TreeNode(-3)
    assert maxPathSum(root) == -1


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
    #    / \
    #   4   5
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    assert maxPathSum(root) == 15  # 4 + 2 + 1 + 3 + 5


def test_path_not_through_root():
    """Test where max path doesn't go through root"""
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
    assert maxPathSum(root) == 42  # 15 + 20 + 7


def test_single_path_down():
    """Test where best path is just going down one side"""
    #     1
    #    /
    #   2
    #  /
    # 3
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.left.left = TreeNode(3)
    assert maxPathSum(root) == 6  # 3 + 2 + 1


def test_negative_branch_ignored():
    """Test where negative branches are ignored"""
    #       10
    #      /  \
    #    -5    5
    root = TreeNode(10)
    root.left = TreeNode(-5)
    root.right = TreeNode(5)
    assert maxPathSum(root) == 15  # 10 + 5 (ignore -5)


def test_empty_tree():
    """Test with None"""
    assert maxPathSum(None) == float('-inf')


def test_large_tree():
    """Test with a larger tree"""
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
    assert maxPathSum(root) == 48  # 7 + 11 + 4 + 5 + 8 + 13
