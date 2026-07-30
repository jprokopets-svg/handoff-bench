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
    The path must contain at least one node and does not need to go through the root.
    
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
        going down to its descendants.
        
        Also updates max_sum with the maximum path sum found so far.
        """
        if not node:
            return 0
        
        # Get the maximum path sum from left and right subtrees
        # We use max(0, ...) because we can choose not to include a negative path
        left_sum = max(0, dfs(node.left))
        right_sum = max(0, dfs(node.right))
        
        # The maximum path that goes through this node
        # includes the node value plus the best paths from left and right
        path_through_node = node.val + left_sum + right_sum
        
        # Update the global maximum
        max_sum[0] = max(max_sum[0], path_through_node)
        
        # Return the maximum path sum starting from this node going down
        # (can only go through one child, not both)
        return node.val + max(left_sum, right_sum)
    
    dfs(root)
    return max_sum[0]
