class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def is_valid_bst(root: TreeNode | None) -> bool:
    def validate(node, min_val, max_val):
        if not node:
            return True
        
        # Check current node against bounds
        if min_val is not None and node.val <= min_val:
            return False
        if max_val is not None and node.val >= max_val:
            return False
        
        # Recursively check left and right subtrees
        return (validate(node.left, min_val, node.val) and 
                validate(node.right, node.val, max_val))
    
    return validate(root, None, None)
