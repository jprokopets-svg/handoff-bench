from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return f"TreeNode({self.val})"


def serialize(root):
    """
    Serialize a binary tree to a string using level-order (BFS) traversal.
    Missing nodes are represented as 'null'.
    
    Example:
        Input tree:
            1
           / \\
          2   3
             / \\
            4   5
        Output: "1,2,3,null,null,4,5"
    """
    if root is None:
        return "null"

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
    The string should be in level-order format with 'null' for missing nodes.
    
    Example:
        Input: "1,2,3,null,null,4,5"
        Output tree:
            1
           / \\
          2   3
             / \\
            4   5
    """
    if not data or data == "null":
        return None

    tokens = data.split(",")
    root = TreeNode(int(tokens[0]))
    queue = deque([root])
    i = 1

    while queue and i < len(tokens):
        node = queue.popleft()

        # Process left child
        if i < len(tokens):
            if tokens[i] != "null":
                node.left = TreeNode(int(tokens[i]))
                queue.append(node.left)
            i += 1

        # Process right child
        if i < len(tokens):
            if tokens[i] != "null":
                node.right = TreeNode(int(tokens[i]))
                queue.append(node.right)
            i += 1

    return root


def trees_are_equal(t1, t2):
    """Helper to check if two trees are structurally identical with same values."""
    if t1 is None and t2 is None:
        return True
    if t1 is None or t2 is None:
        return False
    return (t1.val == t2.val and
            trees_are_equal(t1.left, t2.left) and
            trees_are_equal(t1.right, t2.right))
