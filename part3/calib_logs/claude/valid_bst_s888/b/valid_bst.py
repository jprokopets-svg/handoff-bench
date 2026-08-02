class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def is_valid_bst(root: TreeNode | None) -> bool:
    """
    Validate whether a binary tree is a valid binary search tree.
    
    For every node, all values in its left subtree must be strictly less
    than the node's value, and all values in its right subtree must be
    strictly greater than the node's value.
    
    Args:
        root: The root node of the binary tree (or None)
    
    Returns:
        True if the tree is a valid BST, False otherwise
    """
    def validate(node, min_val, max_val):
        # Base case: empty node is valid
        if node is None:
            return True
        
        # Check if current node violates BST property
        if node.val <= min_val or node.val >= max_val:
            return False
        
        # Recursively validate left and right subtrees
        # Left subtree: all values must be < node.val
        # Right subtree: all values must be > node.val
        return (validate(node.left, min_val, node.val) and
                validate(node.right, node.val, max_val))
    
    # Start with infinite bounds
    return validate(root, float('-inf'), float('inf'))
