class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def max_path_sum(root):
    """
    Find the maximum path sum in a binary tree.
    A path can start and end at any node (does not need to pass through root).
    
    :param root: TreeNode - root of the binary tree
    :return: int - maximum path sum
    """
    if root is None:
        return 0

    max_sum = [float('-inf')]

    def helper(node):
        if node is None:
            return 0

        # Recursively get the max gain from left and right subtrees
        # If the gain is negative, we ignore it (take 0 instead)
        left_gain = max(helper(node.left), 0)
        right_gain = max(helper(node.right), 0)

        # The price of the current path that passes through this node
        current_path_sum = node.val + left_gain + right_gain

        # Update the global maximum
        max_sum[0] = max(max_sum[0], current_path_sum)

        # Return the max gain if we continue the path through this node
        # (we can only choose one direction: left or right)
        return node.val + max(left_gain, right_gain)

    helper(root)
    return max_sum[0]
