# Implementation of BST validity check
from typing import Optional

class TreeNode:
    def __init__(self, val: int, left: Optional['TreeNode']=None, right: Optional['TreeNode']=None):
        self.val = val
        self.left = left
        self.right = right


def is_valid_bst(root: Optional[TreeNode]) -> bool:
    """Return True if the binary tree rooted at `root` is a valid BST.

    A valid BST requires that for every node, all values in the left subtree
    are strictly less than the node's value and all values in the right
    subtree are strictly greater than the node's value.
    """
    def helper(node: Optional[TreeNode], low: float, high: float) -> bool:
        if node is None:
            return True
        val = node.val
        # strict inequalities
        if not (low < val < high):
            return False
        return helper(node.left, low, val) and helper(node.right, val, high)

    return helper(root, float('-inf'), float('inf'))
