"""
Tests for the maxPathSum function.
"""
import pytest
from max_path_sum import TreeNode, maxPathSum


# --- Helper ---
def build_tree(values):
    """Build a binary tree from a level-order list (None = missing node)."""
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


# --- Basic cases ---

def test_single_positive_node():
    root = TreeNode(5)
    assert maxPathSum(root) == 5

def test_single_negative_node():
    root = TreeNode(-3)
    assert maxPathSum(root) == -3

def test_single_zero_node():
    root = TreeNode(0)
    assert maxPathSum(root) == 0

def test_two_nodes_left():
    root = TreeNode(1, TreeNode(2))
    assert maxPathSum(root) == 3

def test_two_nodes_right():
    root = TreeNode(1, None, TreeNode(2))
    assert maxPathSum(root) == 3

def test_two_nodes_negative_child():
    # Best path is just the root
    root = TreeNode(5, TreeNode(-1))
    assert maxPathSum(root) == 5

def test_simple_three_node_tree():
    # Tree:   1
    #        / \
    #       2   3
    # Best path: 2 -> 1 -> 3 = 6
    root = TreeNode(1, TreeNode(2), TreeNode(3))
    assert maxPathSum(root) == 6

# --- LeetCode classic examples ---

def test_leetcode_example_1():
    # [1, 2, 3] => 6
    root = build_tree([1, 2, 3])
    assert maxPathSum(root) == 6

def test_leetcode_example_2():
    # [-10, 9, 20, None, None, 15, 7]
    #        -10
    #        /  \
    #       9   20
    #          /  \
    #         15   7
    # Best path: 15 -> 20 -> 7 = 42
    root = build_tree([-10, 9, 20, None, None, 15, 7])
    assert maxPathSum(root) == 42

# --- All negative values ---

def test_all_negative_returns_least_negative():
    root = TreeNode(-1, TreeNode(-2), TreeNode(-3))
    assert maxPathSum(root) == -1

def test_all_negative_chain():
    # -3 -> -2 -> -1; best single node is -1
    root = TreeNode(-3, TreeNode(-2, TreeNode(-1)))
    assert maxPathSum(root) == -1

def test_two_negative_nodes():
    root = TreeNode(-5, TreeNode(-1))
    assert maxPathSum(root) == -1

# --- Mixed positive/negative ---

def test_best_path_avoids_negative_branch():
    #      10
    #     /  \
    #   -5    5
    # Best path: 10 + 5 = 15
    root = TreeNode(10, TreeNode(-5), TreeNode(5))
    assert maxPathSum(root) == 15

def test_best_path_is_subtree():
    #        -10
    #        /  \
    #       5    4
    #      / \
    #     3   6
    # Best path: 3 -> 5 -> 6 = 14
    root = TreeNode(-10,
                    TreeNode(5, TreeNode(3), TreeNode(6)),
                    TreeNode(4))
    assert maxPathSum(root) == 14

def test_path_does_not_go_through_root():
    #      -5
    #      / \
    #     4   6
    #    / \
    #   3   2
    # Best path: 3 -> 4 -> 2 = 9 (or 4->2=6, 4->3=7, 3->4->2=9)
    root = TreeNode(-5,
                    TreeNode(4, TreeNode(3), TreeNode(2)),
                    TreeNode(6))
    assert maxPathSum(root) == 9

# --- Skewed trees ---

def test_left_skewed_all_positive():
    # 1 -> 2 -> 3 -> 4
    root = TreeNode(1, TreeNode(2, TreeNode(3, TreeNode(4))))
    assert maxPathSum(root) == 10

def test_right_skewed_all_positive():
    root = TreeNode(1, None, TreeNode(2, None, TreeNode(3, None, TreeNode(4))))
    assert maxPathSum(root) == 10

def test_left_skewed_mixed():
    # Best path might be a sub-chain
    root = TreeNode(-1, TreeNode(3, TreeNode(-2, TreeNode(5))))
    # Paths: -1+3=2, 3, 3-2=1, -2+5=3, 5, -2, -1, -1+3-2+5=5, 3-2+5=6
    assert maxPathSum(root) == 6

# --- Larger / deeper trees ---

def test_balanced_tree_deep():
    #         1
    #       /   \
    #      2     3
    #     / \   / \
    #    4   5 6   7
    # Best path: 4->2->5 = 11, or 6->3->7 = 16, or 4->2->1->3->7 = 17
    root = build_tree([1, 2, 3, 4, 5, 6, 7])
    assert maxPathSum(root) == 18  # 4+2+5+1+3+7 = no, path can't fork twice
    # Actually: path through root: left_best=max(4+2,5+2)=6+2? 
    # Let's recalculate: left subtree best down = max(4,5)+2=7, right=max(6,7)+3=10
    # path through root = 7+1+10 = 18
    # path through node2 = 4+2+5 = 11
    # path through node3 = 6+3+7 = 16
    # global max = 18

def test_single_path_best():
    #    5
    #   /
    #  4
    #   \
    #    3
    root = TreeNode(5, TreeNode(4, None, TreeNode(3)))
    assert maxPathSum(root) == 12

def test_large_values():
    root = TreeNode(1000, TreeNode(1000), TreeNode(1000))
    assert maxPathSum(root) == 3000

def test_zero_values():
    root = TreeNode(0, TreeNode(0), TreeNode(0))
    assert maxPathSum(root) == 0

def test_mixed_with_zeros():
    root = TreeNode(0, TreeNode(5), TreeNode(-1))
    assert maxPathSum(root) == 5

# --- Empty tree ---

def test_empty_tree():
    assert maxPathSum(None) == 0
