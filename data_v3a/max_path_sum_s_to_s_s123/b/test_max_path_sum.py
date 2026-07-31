import pytest
from max_path_sum import TreeNode, max_path_sum


def build_tree(values):
    """Build a binary tree from a list (level-order). None means no node."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    while queue and i < len(values):
        node = queue.pop(0)
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root


def test_single_node():
    root = TreeNode(5)
    assert max_path_sum(root) == 5


def test_single_negative_node():
    root = TreeNode(-3)
    assert max_path_sum(root) == -3


def test_simple_tree():
    # Tree:   1
    #        / \
    #       2   3
    root = build_tree([1, 2, 3])
    assert max_path_sum(root) == 6  # 2 -> 1 -> 3


def test_negative_children():
    # Tree:   1
    #        / \
    #      -2  -3
    root = build_tree([1, -2, -3])
    assert max_path_sum(root) == 1  # just the root


def test_example_with_negatives():
    # Tree:  -10
    #        /  \
    #       9   20
    #          /  \
    #         15   7
    root = TreeNode(-10)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    assert max_path_sum(root) == 42  # 15 -> 20 -> 7


def test_all_negative():
    # Tree:  -1
    #        / \
    #      -2  -3
    root = build_tree([-1, -2, -3])
    assert max_path_sum(root) == -1  # best single node


def test_left_skewed():
    # Tree: 1 -> 2 -> 3 (left-skewed)
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.left.left = TreeNode(3)
    assert max_path_sum(root) == 6  # 3 -> 2 -> 1


def test_path_not_through_root():
    # Tree:   -5
    #         / \
    #        4   8
    #       / \
    #      11  13
    #     /  \
    #    7    2
    root = TreeNode(-5)
    root.left = TreeNode(4)
    root.right = TreeNode(8)
    root.left.left = TreeNode(11)
    root.left.right = TreeNode(13)
    root.left.left.left = TreeNode(7)
    root.left.left.right = TreeNode(2)
    # Best path: 7 -> 11 -> 4 -> 13 = 35? No: 7+11+4+13=35, or 7+11+2=20
    # Actually: 7 -> 11 -> 4 -> 13 is not a valid path (can't branch)
    # Valid paths: 7->11->4->13 is invalid (branching)
    # 7->11->2 = 20, 13->4->11->7 = 35, 13->4->11->2 = 30
    # Best: 13 -> 4 -> 11 -> 7 = 35
    assert max_path_sum(root) == 35


def test_none_root():
    assert max_path_sum(None) == 0


def test_two_nodes():
    root = TreeNode(1)
    root.left = TreeNode(2)
    assert max_path_sum(root) == 3


def test_large_values():
    root = TreeNode(1000)
    root.left = TreeNode(1000)
    root.right = TreeNode(1000)
    assert max_path_sum(root) == 3000
