"""
Test cases for maximum path sum in binary tree
"""

from max_path_sum import TreeNode, maxPathSum


def test_single_node():
    """Test with a single node"""
    root = TreeNode(1)
    assert maxPathSum(root) == 1


def test_two_nodes():
    """Test with two nodes"""
    root = TreeNode(1)
    root.left = TreeNode(2)
    assert maxPathSum(root) == 3


def test_three_nodes_linear():
    """Test with three nodes in a line"""
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    assert maxPathSum(root) == 6


def test_negative_values():
    """Test with negative values - path should be 15+20+7=42"""
    root = TreeNode(-10)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    assert maxPathSum(root) == 42


def test_all_negative():
    """Test with all negative values - should return the least negative"""
    root = TreeNode(-3)
    assert maxPathSum(root) == -3


def test_all_negative_multiple():
    """Test with multiple negative nodes"""
    root = TreeNode(-2)
    root.left = TreeNode(-1)
    assert maxPathSum(root) == -1


def test_complex_tree():
    """Test with a more complex tree"""
    #       1
    #      / \
    #     2   3
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    assert maxPathSum(root) == 6


def test_path_not_through_root():
    """Test where max path doesn't go through root"""
    #       -10
    #       /  \
    #      5    5
    #     /      \
    #    3        4
    root = TreeNode(-10)
    root.left = TreeNode(5)
    root.right = TreeNode(5)
    root.left.left = TreeNode(3)
    root.right.right = TreeNode(4)
    # Max path is 5 + 3 = 8 (left subtree)
    assert maxPathSum(root) == 8


def test_empty_tree():
    """Test with empty tree"""
    assert maxPathSum(None) == 0


def test_single_negative_node():
    """Test single negative node"""
    root = TreeNode(-5)
    assert maxPathSum(root) == -5
