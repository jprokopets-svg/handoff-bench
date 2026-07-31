"""
Tests for Maximum Path Sum in Binary Tree
"""
import pytest
from max_path_sum import TreeNode, maxPathSum


def test_basic_three_nodes():
    # Tree:   1
    #        / \
    #       2   3
    # Max path: 2 -> 1 -> 3 = 6
    root = TreeNode(1, TreeNode(2), TreeNode(3))
    assert maxPathSum(root) == 6


def test_single_node_positive():
    root = TreeNode(5)
    assert maxPathSum(root) == 5


def test_single_node_negative():
    root = TreeNode(-3)
    assert maxPathSum(root) == -3


def test_all_negative():
    # Tree:   -1
    #        /  \
    #       -2  -3
    # Max path: just -1
    root = TreeNode(-1, TreeNode(-2), TreeNode(-3))
    assert maxPathSum(root) == -1


def test_mixed_positive_negative():
    # Tree:    -10
    #          /  \
    #         9   20
    #            /  \
    #           15   7
    # Max path: 15 -> 20 -> 7 = 42
    root = TreeNode(-10,
                    TreeNode(9),
                    TreeNode(20, TreeNode(15), TreeNode(7)))
    assert maxPathSum(root) == 42


def test_path_does_not_include_root():
    # Tree:    1
    #         / \
    #        2   3
    #       / \
    #      4   5
    # Max path: 4 -> 2 -> 5 = 11
    root = TreeNode(1,
                    TreeNode(2, TreeNode(4), TreeNode(5)),
                    TreeNode(3))
    assert maxPathSum(root) == 11


def test_left_skewed_tree():
    # Tree:  1
    #       /
    #      2
    #     /
    #    3
    # Max path: 1 -> 2 -> 3 = 6
    root = TreeNode(1, TreeNode(2, TreeNode(3)))
    assert maxPathSum(root) == 6


def test_right_skewed_tree():
    # Tree:  1
    #         \
    #          2
    #           \
    #            3
    # Max path: 1 -> 2 -> 3 = 6
    root = TreeNode(1, None, TreeNode(2, None, TreeNode(3)))
    assert maxPathSum(root) == 6


def test_negative_children_single_best_node():
    # Tree:   5
    #        / \
    #      -1  -2
    # Max path: just 5 (ignoring negative children)
    root = TreeNode(5, TreeNode(-1), TreeNode(-2))
    assert maxPathSum(root) == 5


def test_large_values():
    # Tree:   100
    #        /   \
    #      200   300
    # Max path: 200 -> 100 -> 300 = 600
    root = TreeNode(100, TreeNode(200), TreeNode(300))
    assert maxPathSum(root) == 600


def test_path_through_leaf():
    # Tree:    2
    #         / \
    #        1   3
    #       /
    #     -1
    # Max path: 1 -> 2 -> 3 = 6
    root = TreeNode(2,
                    TreeNode(1, TreeNode(-1)),
                    TreeNode(3))
    assert maxPathSum(root) == 6


def test_two_nodes_left():
    # Tree:  1
    #       /
    #      2
    # Max path: 1 -> 2 = 3
    root = TreeNode(1, TreeNode(2))
    assert maxPathSum(root) == 3


def test_two_nodes_right():
    # Tree:  1
    #         \
    #          2
    # Max path: 1 -> 2 = 3
    root = TreeNode(1, None, TreeNode(2))
    assert maxPathSum(root) == 3


def test_all_same_values():
    # Tree:   3
    #        / \
    #       3   3
    # Max path: 3 -> 3 -> 3 = 9
    root = TreeNode(3, TreeNode(3), TreeNode(3))
    assert maxPathSum(root) == 9


def test_none_root():
    assert maxPathSum(None) == 0
