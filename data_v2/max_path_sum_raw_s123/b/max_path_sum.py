"""
Maximum Path Sum in Binary Tree

A path can start and end at any node in the tree.
The path must be continuous (following parent-child relationships).
"""

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def maxPathSum(root):
    """
    Find the maximum path sum in a binary tree.
    
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
        DFS helper function that returns the maximum path sum ending at this node.
        Also updates the global maximum path sum.
        
        Args:
            node: TreeNode - current node
            
        Returns:
            int - maximum path sum that ends at this node (going down)
        """
        if not node:
            return 0
        
        # Get max path sum from left and right subtrees
        # We use max(0, ...) because we can choose not to include a negative path
        left_sum = max(0, dfs(node.left))
        right_sum = max(0, dfs(node.right))
        
        # Maximum path sum that passes through this node
        # (could go left -> node -> right)
        path_through_node = node.val + left_sum + right_sum
        
        # Update global maximum
        max_sum[0] = max(max_sum[0], path_through_node)
        
        # Return the maximum path sum that ends at this node
        # (either goes left or right, not both)
        return node.val + max(left_sum, right_sum)
    
    dfs(root)
    return max_sum[0]
