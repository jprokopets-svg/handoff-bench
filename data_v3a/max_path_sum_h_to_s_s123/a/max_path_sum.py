"""
Maximum Path Sum in Binary Tree

A path can start and end at any node in the tree.
The path must follow parent-child connections.
"""

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def maxPathSum(root):
    """
    Find the maximum path sum in a binary tree.
    
    A path can start and end at any node. The path must follow
    parent-child connections (cannot skip nodes).
    
    Args:
        root: TreeNode - root of the binary tree
        
    Returns:
        int - the maximum path sum
    """
    if not root:
        return 0
    
    max_sum = float('-inf')
    
    def dfs(node):
        nonlocal max_sum
        
        if not node:
            return 0
        
        # Get max path sum from left and right subtrees
        # We use max(0, ...) because we can choose not to include a negative path
        left_sum = max(0, dfs(node.left))
        right_sum = max(0, dfs(node.right))
        
        # Max path sum that goes through this node
        # (can include left subtree, right subtree, or both)
        current_max = node.val + left_sum + right_sum
        max_sum = max(max_sum, current_max)
        
        # Return the max path sum that can be extended to parent
        # (can only go through one child, not both)
        return node.val + max(left_sum, right_sum)
    
    dfs(root)
    return max_sum
