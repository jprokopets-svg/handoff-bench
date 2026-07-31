import pytest
from max_path_sum import TreeNode, max_path_sum


def build_tree(values):
    """Helper to build a binary tree from a list (level-order, None for missing nodes)."""
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


class TestMaxPathSum:

    def test_single_node(self):
        root = TreeNode(5)
        assert max_path_sum(root) == 5

    def test_single_negative_node(self):
        root = TreeNode(-3)
        assert max_path_sum(root) == -3

    def test_simple_tree(self):
        # Tree:   1
        #        / \
        #       2   3
        # Max path: 2 -> 1 -> 3 = 6
        root = build_tree([1, 2, 3])
        assert max_path_sum(root) == 6

    def test_path_through_root(self):
        # Tree:  -10
        #        /  \
        #       9   20
        #          /  \
        #         15   7
        # Max path: 15 -> 20 -> 7 = 42
        root = build_tree([-10, 9, 20, None, None, 15, 7])
        assert max_path_sum(root) == 42

    def test_all_negative(self):
        # Tree:  -1
        #        / \
        #      -2  -3
        # Max path is just -1 (the root)
        root = build_tree([-1, -2, -3])
        assert max_path_sum(root) == -1

    def test_left_skewed(self):
        # Tree: 1 -> 2 -> 3 (left skewed)
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.left.left = TreeNode(3)
        # Max path: 1 + 2 + 3 = 6
        assert max_path_sum(root) == 6

    def test_right_skewed(self):
        # Tree: 1 -> 2 -> 3 (right skewed)
        root = TreeNode(1)
        root.right = TreeNode(2)
        root.right.right = TreeNode(3)
        assert max_path_sum(root) == 6

    def test_best_path_not_through_root(self):
        # Tree:    1
        #         / \
        #        5   3
        #       / \
        #      4   6
        # Max path: 4 -> 5 -> 6 = 15
        root = TreeNode(1)
        root.left = TreeNode(5)
        root.right = TreeNode(3)
        root.left.left = TreeNode(4)
        root.left.right = TreeNode(6)
        assert max_path_sum(root) == 15

    def test_mixed_positive_negative(self):
        # Tree:   2
        #        / \
        #      -1   3
        # Max path: 2 -> 3 = 5
        root = build_tree([2, -1, 3])
        assert max_path_sum(root) == 5

    def test_large_values(self):
        root = TreeNode(1000)
        root.left = TreeNode(1000)
        root.right = TreeNode(1000)
        assert max_path_sum(root) == 3000

    def test_zero_node(self):
        root = TreeNode(0)
        root.left = TreeNode(5)
        root.right = TreeNode(10)
        # Max path: 5 -> 0 -> 10 = 15
        assert max_path_sum(root) == 15

    def test_empty_tree(self):
        assert max_path_sum(None) == 0
