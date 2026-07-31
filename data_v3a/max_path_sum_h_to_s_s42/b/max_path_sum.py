"""
Maximum Path Sum in Binary Tree

A path can start and end at any node in the tree.
"""

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def maxPathSum(root):
    """
    Find the maximum path sum in a binary tree.
    
    A path can start and end at any node. The path must contain at least one node
    and does not need to go through the root.
    
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
        DFS helper function that returns the maximum path sum starting from this node
        and going down to its descendants.
        
        Also updates the global max_sum with the maximum path sum found so far.
        """
        if not node:
            return 0
        
        # Get the maximum path sum from left and right subtrees
        # We use max(0, ...) because we can choose not to include a path if it's negative
        left_sum = max(0, dfs(node.left))
        right_sum = max(0, dfs(node.right))
        
        # The maximum path sum that passes through this node
        # includes the node value plus the best paths from left and right
        current_max = node.val + left_sum + right_sum
        
        # Update the global maximum
        max_sum[0] = max(max_sum[0], current_max)
        
        # Return the maximum path sum starting from this node going down
        # (can only go through one child, not both)
        return node.val + max(left_sum, right_sum)
    
    dfs(root)
    return max_sum[0]
