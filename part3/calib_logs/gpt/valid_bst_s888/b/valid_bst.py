class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return f"TreeNode({self.val})"


def is_valid_bst(root: TreeNode | None) -> bool:
    """Iterative check using explicit stack with (node, low, high) bounds.

    For each node ensure low < node.val < high. Bounds are strict: duplicates
    are considered invalid.
    """
    if root is None:
        return True

    import math
    NEG_INF = -math.inf
    POS_INF = math.inf

    stack = [(root, NEG_INF, POS_INF)]
    while stack:
        node, low, high = stack.pop()
        if node is None:
            continue
        val = node.val
        # must satisfy strict inequalities
        if not (low < val < high):
            return False
        # right subtree must be > val
        if node.right is not None:
            stack.append((node.right, val, high))
        # left subtree must be < val
        if node.left is not None:
            stack.append((node.left, low, val))
    return True
