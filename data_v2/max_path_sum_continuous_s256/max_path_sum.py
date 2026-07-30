class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def max_path_sum(root):
    """
    Find the maximum path sum in a binary tree.
    A path can start and end at any node.
    
    Args:
        root: TreeNode - the root of the binary tree
        
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
        
        # Get the maximum sum from left and right subtrees
        # Use max(0, ...) to ignore negative paths
        left_sum = max(0, dfs(node.left))
        right_sum = max(0, dfs(node.right))
        
        # Calculate the maximum path sum that passes through this node
        current_path_sum = node.val + left_sum + right_sum
        
        # Update the global maximum
        max_sum = max(max_sum, current_path_sum)
        
        # Return the maximum sum of a path that goes through this node
        # and continues to one of its children (or just this node)
        return node.val + max(left_sum, right_sum)
    
    dfs(root)
    return max_sum
