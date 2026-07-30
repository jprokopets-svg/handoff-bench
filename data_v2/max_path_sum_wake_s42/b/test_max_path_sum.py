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
    assert maxPathSum(root) == -1


def test_mixed_values():
    """Test with mixed positive and negative values"""
    #       1
    #      / \
    #     2   3
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    assert maxPathSum(root) == 6


def test_complex_tree():
    """Test with a more complex tree"""
    #        -10
    #        /  \
    #       9   20
    #          /  \
    #         15   7
    root = TreeNode(-10)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    assert maxPathSum(root) == 42  # 15 + 20 + 7


def test_single_path():
    """Test where max path is a single path down the tree"""
    #       1
    #      /
    #     2
    #    /
    #   3
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.left.left = TreeNode(3)
    assert maxPathSum(root) == 6


def test_path_through_root():
    """Test where max path goes through root"""
    #       10
    #      /  \
    #     5    5
    #    /      \
    #   3        3
    root = TreeNode(10)
    root.left = TreeNode(5)
    root.right = TreeNode(5)
    root.left.left = TreeNode(3)
    root.right.right = TreeNode(3)
    assert maxPathSum(root) == 26  # 3 + 5 + 10 + 5 + 3


def test_negative_branch_ignored():
    """Test where negative branch is ignored"""
    #       5
    #      / \
    #    -10  3
    root = TreeNode(5)
    root.left = TreeNode(-10)
    root.right = TreeNode(3)
    assert maxPathSum(root) == 8  # 5 + 3, ignoring -10
