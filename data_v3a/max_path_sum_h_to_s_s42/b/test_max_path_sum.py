"""
Tests for Maximum Path Sum in Binary Tree
"""
import pytest
from max_path_sum import maxPathSum, TreeNode


def build_tree(values):
    """Helper to build a binary tree from a level-order list. None means no node."""
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

    def test_empty_tree(self):
        """Empty tree should return 0."""
        assert maxPathSum(None) == 0

    def test_single_node_positive(self):
        """Single node with positive value."""
        root = TreeNode(5)
        assert maxPathSum(root) == 5

    def test_single_node_negative(self):
        """Single node with negative value — must include it (only node)."""
        root = TreeNode(-3)
        assert maxPathSum(root) == -3

    def test_single_node_zero(self):
        """Single node with zero value."""
        root = TreeNode(0)
        assert maxPathSum(root) == 0

    def test_simple_tree_positive(self):
        """
        Simple tree:
             1
            / \
           2   3
        Max path: 2 -> 1 -> 3 = 6
        """
        root = build_tree([1, 2, 3])
        assert maxPathSum(root) == 6

    def test_leetcode_example_1(self):
        """
        LeetCode example 1:
             -10
            /   \
           9    20
               /  \
              15   7
        Max path: 15 -> 20 -> 7 = 42
        """
        root = build_tree([-10, 9, 20, None, None, 15, 7])
        assert maxPathSum(root) == 42

    def test_all_negative(self):
        """
        All negative values — must pick the least negative single node.
             -3
            /  \
          -2   -1
        Max path: -1 (single node)
        """
        root = build_tree([-3, -2, -1])
        assert maxPathSum(root) == -1

    def test_all_negative_single_path(self):
        """
        All negative, linear tree:
        -1 -> -2 -> -3
        Max path: -1
        """
        root = TreeNode(-1)
        root.left = TreeNode(-2)
        root.left.left = TreeNode(-3)
        assert maxPathSum(root) == -1

    def test_path_does_not_go_through_root(self):
        """
        Max path doesn't include root:
              -5
             /   \
            4     6
           / \
          3   2
        Max path: 3 -> 4 -> 2 = 9
        """
        root = TreeNode(-5)
        root.left = TreeNode(4)
        root.right = TreeNode(6)
        root.left.left = TreeNode(3)
        root.left.right = TreeNode(2)
        assert maxPathSum(root) == 9

    def test_left_skewed_tree(self):
        """
        Left-skewed tree:
        1 -> 2 -> 3 -> 4
        Max path: 1+2+3+4 = 10
        """
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.left.left = TreeNode(3)
        root.left.left.left = TreeNode(4)
        assert maxPathSum(root) == 10

    def test_right_skewed_tree(self):
        """
        Right-skewed tree:
        1 -> 2 -> 3
        Max path: 1+2+3 = 6
        """
        root = TreeNode(1)
        root.right = TreeNode(2)
        root.right.right = TreeNode(3)
        assert maxPathSum(root) == 6

    def test_mixed_positive_negative(self):
        """
        Mixed values:
             2
            / \
          -1   3
        Max path: 2 -> 3 = 5
        """
        root = build_tree([2, -1, 3])
        assert maxPathSum(root) == 5

    def test_large_values(self):
        """
        Tree with large values:
             1000
            /    \
          500    500
        Max path: 500 + 1000 + 500 = 2000
        """
        root = build_tree([1000, 500, 500])
        assert maxPathSum(root) == 2000

    def test_path_is_single_leaf(self):
        """
        When the best path is a single leaf node:
             -10
            /   \
          -5    100
        Max path: 100
        """
        root = build_tree([-10, -5, 100])
        assert maxPathSum(root) == 100

    def test_deeper_tree(self):
        """
        Deeper tree where path goes through multiple levels:
                1
               / \
              2   3
             / \
            4   5
        Max path: 4 -> 2 -> 5 = 11 (or 4->2->1->3=10, so 11 wins)
        """
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        root.left.left = TreeNode(4)
        root.left.right = TreeNode(5)
        assert maxPathSum(root) == 11

    def test_negative_root_positive_children(self):
        """
        Negative root, positive children:
             -1
            /  \
           5    4
        Max path: 5 -> (-1) -> 4 = 8
        """
        root = build_tree([-1, 5, 4])
        assert maxPathSum(root) == 8

    def test_zigzag_path_not_valid(self):
        """
        A valid path cannot zigzag — it must be a straight downward path or go
        through a node connecting two downward paths.
              1
             / \
            2   3
           /     \
          4       5
        Max path: 4->2->1->3->5 = 15
        """
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        root.left.left = TreeNode(4)
        root.right.right = TreeNode(5)
        assert maxPathSum(root) == 15
