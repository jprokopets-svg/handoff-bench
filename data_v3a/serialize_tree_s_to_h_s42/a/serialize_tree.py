from collections import deque


class TreeNode:
    """Definition for a binary tree node."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return f"TreeNode({self.val})"


def serialize(root):
    """
    Serialize a binary tree to a string using level-order (BFS) traversal.
    Null nodes are represented as 'null'.

    Args:
        root (TreeNode | None): The root of the binary tree.

    Returns:
        str: A comma-separated string representation of the tree.

    Example:
        >>> root = TreeNode(1, TreeNode(2), TreeNode(3))
        >>> serialize(root)
        '1,2,3'
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

    # Strip trailing 'null' values for a cleaner representation
    while result and result[-1] == "null":
        result.pop()

    return ",".join(result)


def deserialize(data):
    """
    Deserialize a string back to a binary tree.

    Args:
        data (str): A comma-separated string produced by serialize().

    Returns:
        TreeNode | None: The root of the reconstructed binary tree.

    Example:
        >>> root = deserialize('1,2,3')
        >>> root.val
        1
        >>> root.left.val
        2
        >>> root.right.val
        3
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

        # Assign left child
        if i < len(tokens):
            if tokens[i] != "null":
                node.left = TreeNode(int(tokens[i]))
                queue.append(node.left)
            i += 1

        # Assign right child
        if i < len(tokens):
            if tokens[i] != "null":
                node.right = TreeNode(int(tokens[i]))
                queue.append(node.right)
            i += 1

    return root
