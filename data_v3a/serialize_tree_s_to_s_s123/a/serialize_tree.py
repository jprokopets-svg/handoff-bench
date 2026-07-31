from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __eq__(self, other):
        if self is None and other is None:
            return True
        if self is None or other is None:
            return False
        return (self.val == other.val and
                self.left == other.left and
                self.right == other.right)

    def __repr__(self):
        return f"TreeNode({self.val})"


def serialize(root):
    """Serialize a binary tree to a string using level-order traversal.
    
    Args:
        root: TreeNode or None - the root of the binary tree
        
    Returns:
        str: A comma-separated string representation, e.g. "1,2,3,null,null,4,5"
    """
    if root is None:
        return ""

    result = []
    queue = deque([root])

    while queue:
        node = queue.popleft()
        if node is None:
            result.append("null")
        else:
            result.append(str(node.val))
            queue.append(node.left)
            queue.append(node.right)

    # Remove trailing 'null' values for a cleaner representation
    while result and result[-1] == "null":
        result.pop()

    return ",".join(result)


def deserialize(data):
    """Deserialize a string back to a binary tree.
    
    Args:
        data: str - A comma-separated string as produced by serialize()
        
    Returns:
        TreeNode or None - the root of the reconstructed binary tree
    """
    if not data or data.strip() == "":
        return None

    tokens = data.split(",")
    if not tokens or tokens[0] == "null":
        return None

    root = TreeNode(int(tokens[0]))
    queue = deque([root])
    i = 1

    while queue and i < len(tokens):
        node = queue.popleft()

        # Left child
        if i < len(tokens):
            if tokens[i] != "null":
                node.left = TreeNode(int(tokens[i]))
                queue.append(node.left)
            i += 1

        # Right child
        if i < len(tokens):
            if tokens[i] != "null":
                node.right = TreeNode(int(tokens[i]))
                queue.append(node.right)
            i += 1

    return root
