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
        root: TreeNode - the root of the binary tree
        
    Returns:
        int - the maximum path sum
    """
    if not root:
        return 0
    
    max_sum = [float('-inf')]
    
    def dfs(node):
        """
        DFS helper function that returns the maximum path sum
        starting from this node and going down to its descendants.
        
        Also updates max_sum with the maximum path sum found so far.
        """
        if not node:
            return 0
        
        # Get the maximum path sum from left and right subtrees
        # Use max(0, ...) to ignore negative paths
        left_sum = max(0, dfs(node.left))
        right_sum = max(0, dfs(node.right))
        
        # Maximum path sum that passes through this node
        # (can go left, right, or both)
        path_through_node = node.val + left_sum + right_sum
        max_sum[0] = max(max_sum[0], path_through_node)
        
        # Return the maximum path sum starting from this node
        # going down to one of its subtrees (not both, as we need a path)
        return node.val + max(left_sum, right_sum)
    
    dfs(root)
    return max_sum[0]
