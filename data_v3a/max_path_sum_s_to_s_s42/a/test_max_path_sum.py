import pytest
from max_path_sum import TreeNode, max_path_sum


def test_single_node():
    root = TreeNode(5)
    assert max_path_sum(root) == 5


def test_single_negative_node():
    root = TreeNode(-3)
    assert max_path_sum(root) == -3


def test_simple_tree():
    # Tree:
    #     1
    #    / \
    #   2   3
    root = TreeNode(1, TreeNode(2), TreeNode(3))
    assert max_path_sum(root) == 6


def test_negative_values():
    # Tree:
    #     -10
    #    /   \
    #   9    20
    #       /  \
    #      15   7
    root = TreeNode(-10,
                    TreeNode(9),
                    TreeNode(20, TreeNode(15), TreeNode(7)))
    assert max_path_sum(root) == 42  # 15 -> 20 -> 7


def test_all_negative():
    # Tree:
    #    -1
    #   /  \
    # -2   -3
    root = TreeNode(-1, TreeNode(-2), TreeNode(-3))
    assert max_path_sum(root) == -1


def test_left_skewed():
    # Tree:
    #   1
    #  /
    # 2
    #  \
    #   3
    root = TreeNode(1, TreeNode(2, None, TreeNode(3)), None)
    assert max_path_sum(root) == 6  # 1 -> 2 -> 3


def test_path_not_through_root():
    # Tree:
    #      1
    #     / \
    #   -1  -1
    #   / \
    #  5   6
    # Best path: 5 -> -1 -> 6 = 10
    root = TreeNode(1,
                    TreeNode(-1, TreeNode(5), TreeNode(6)),
                    TreeNode(-1))
    assert max_path_sum(root) == 10  # 5 -> -1 -> 6


def test_empty_tree():
    assert max_path_sum(None) == 0


def test_two_nodes():
    root = TreeNode(1, TreeNode(2), None)
    assert max_path_sum(root) == 3


def test_large_values():
    root = TreeNode(100, TreeNode(200), TreeNode(300))
    assert max_path_sum(root) == 600
