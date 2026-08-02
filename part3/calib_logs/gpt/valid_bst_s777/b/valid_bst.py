class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return f"TreeNode({self.val!r}, {self.left!r}, {self.right!r})"


def is_valid_bst(root: TreeNode | None) -> bool:
    """Iterative in-order traversal: values must be strictly increasing.
    This avoids recursion depth issues.
    """
    prev = None
    stack = []
    node = root
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        if prev is not None and node.val <= prev:
            return False
        prev = node.val
        node = node.right
    return True
