from typing import Optional

class TreeNode:
    def __init__(self, val: int, left: 'TreeNode' = None, right: 'TreeNode' = None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return f"TreeNode({self.val}, {self.left!r}, {self.right!r})"


def is_valid_bst(root: Optional[TreeNode]) -> bool:
    """Return True if the binary tree is a valid BST.

    For every node, all values in its left subtree must be strictly less than the node's
    value and all values in its right subtree must be strictly greater.
    """
    def helper(node: Optional[TreeNode], low, high) -> bool:
        if node is None:
            return True
        val = node.val
        # must satisfy low < val < high (strict)
        if not (low < val < high):
            return False
        return helper(node.left, low, val) and helper(node.right, val, high)

    return helper(root, float('-inf'), float('inf'))
