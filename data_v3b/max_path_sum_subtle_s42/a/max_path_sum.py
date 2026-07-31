"""
Solution for finding the maximum path sum in a binary tree.
A path can start and end at any node.
"""

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def maxPathSum(root):
    """
    Find the maximum path sum in a binary tree.
    
    A path can start and end at any node in the tree.
    The path must contain at least one node.
    
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
        starting from the given node and going down.
        
        Also updates max_sum with the maximum path sum found so far.
        """
        if not node:
            return 0
        
        # Get the maximum sum from left and right subtrees
        # Use max(0, ...) to ignore negative paths
        left_sum = max(0, dfs(node.left))
        right_sum = max(0, dfs(node.right))
        
        # Calculate the maximum path sum that passes through this node
        # This includes the node itself plus the best paths from left and right
        current_max = node.val + left_sum + right_sum
        
        # Update the global maximum
        max_sum[0] = max(max_sum[0], current_max)
        
        # Return the maximum path sum starting from this node going down
        # (either through left or right, not both)
        return node.val + max(left_sum, right_sum)
    
    dfs(root)
    return max_sum[0]
