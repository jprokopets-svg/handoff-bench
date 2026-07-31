import pytest
from max_path_sum import TreeNode, max_path_sum


def test_single_node():
    root = TreeNode(5)
    assert max_path_sum(root) == 5


def test_single_negative_node():
    root = TreeNode(-3)
    assert max_path_sum(root) == -3


def test_simple_tree():
    # Tree:    1
    #         / \
    #        2   3
    # Max path: 2 -> 1 -> 3 = 6
    root = TreeNode(1, TreeNode(2), TreeNode(3))
    assert max_path_sum(root) == 6


def test_negative_children():
    # Tree:    1
    #         / \
    #       -2  -3
    # Max path: just node 1 = 1
    root = TreeNode(1, TreeNode(-2), TreeNode(-3))
    assert max_path_sum(root) == 1


def test_all_negative():
    # Tree:   -1
    #         / \
    #       -2  -3
    # Max path: just node -1 = -1
    root = TreeNode(-1, TreeNode(-2), TreeNode(-3))
    assert max_path_sum(root) == -1


def test_left_skewed():
    # Tree:  1
    #       /
    #      2
    #     /
    #    3
    # Max path: 1 -> 2 -> 3 = 6
    root = TreeNode(1, TreeNode(2, TreeNode(3)))
    assert max_path_sum(root) == 6


def test_right_skewed():
    # Tree: 1
    #        \
    #         2
    #          \
    #           3
    # Max path: 1 -> 2 -> 3 = 6
    root = TreeNode(1, None, TreeNode(2, None, TreeNode(3)))
    assert max_path_sum(root) == 6


def test_path_not_through_root():
    # Tree:      -10
    #            /  \
    #           9   20
    #              /  \
    #             15   7
    # Max path: 15 -> 20 -> 7 = 42
    root = TreeNode(-10, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
    assert max_path_sum(root) == 42


def test_large_values():
    # Tree:   100
    #         / \
    #        50  50
    root = TreeNode(100, TreeNode(50), TreeNode(50))
    assert max_path_sum(root) == 200


def test_path_is_single_leaf():
    # Tree:   -5
    #         / \
    #       -3  -1
    # Max path: just -1
    root = TreeNode(-5, TreeNode(-3), TreeNode(-1))
    assert max_path_sum(root) == -1


def test_empty_tree():
    assert max_path_sum(None) == 0


def test_complex_tree():
    # Tree:        5
    #             / \
    #            4   8
    #           /   / \
    #          11  13   4
    #         /  \       \
    #        7    2       1
    # Max path: 7 -> 11 -> 4 -> 5 -> 8 -> 13 = 48? 
    # Actually: 7+11+4+5+8+13 = 48
    root = TreeNode(5,
                    TreeNode(4,
                             TreeNode(11, TreeNode(7), TreeNode(2))),
                    TreeNode(8,
                             TreeNode(13),
                             TreeNode(4, None, TreeNode(1))))
    assert max_path_sum(root) == 48
