"""
Maximum Path Sum in Binary Tree

A path can start and end at any node in the tree.
The path must go through at least one node.
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
        going down to its children.
        
        Returns the maximum sum of a path that starts at this node and goes down.
        Updates max_sum with the maximum path sum found so far (which may go through this node).
        """
        if not node:
            return 0
        
        # Get the maximum path sum from left and right subtrees
        # We use max(0, ...) because we can choose not to include a path if it's negative
        left_sum = max(0, dfs(node.left))
        right_sum = max(0, dfs(node.right))
        
        # The maximum path through this node includes:
        # - the node's value
        # - the best path from left subtree (if positive)
        # - the best path from right subtree (if positive)
        path_through_node = node.val + left_sum + right_sum
        
        # Update the global maximum
        max_sum[0] = max(max_sum[0], path_through_node)
        
        # Return the maximum path sum that starts at this node and goes down
        # (either through left or right, not both, since a path is linear)
        return node.val + max(left_sum, right_sum)
    
    dfs(root)
    return max_sum[0]
