class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def max_path_sum(root: TreeNode | None) -> int:
    """
    Find the maximum path sum in a binary tree.
    A path can start and end at any node.
    """
    if root is None:
        return float('-inf')
    
    max_sum = float('-inf')
    
    def dfs(node):
        nonlocal max_sum
        
        if node is None:
            return 0
        
        # Get the maximum sum from left and right subtrees
        # Use max(0, ...) to ignore paths that would decrease the sum
        left_sum = max(0, dfs(node.left))
        right_sum = max(0, dfs(node.right))
        
        # The maximum path through this node includes:
        # node value + left subtree max + right subtree max
        current_max = node.val + left_sum + right_sum
        
        # Update global maximum
        max_sum = max(max_sum, current_max)
        
        # Return the maximum sum of a path that goes through this node
        # and extends to one of its children (or just this node)
        return node.val + max(left_sum, right_sum)
    
    dfs(root)
    return max_sum
