from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def serialize(root):
    """
    Serialize a binary tree to a string using level-order traversal.
    Missing nodes are represented as 'null'.
    
    Args:
        root: TreeNode or None - the root of the binary tree
        
    Returns:
        str - serialized tree in format '[val1,val2,null,val3,...]'
    """
    if not root:
        return '[]'
    
    result = []
    queue = deque([root])
    
    while queue:
        node = queue.popleft()
        
        if node is None:
            result.append('null')
        else:
            result.append(str(node.val))
            queue.append(node.left)
            queue.append(node.right)
    
    # Remove trailing nulls
    while result and result[-1] == 'null':
        result.pop()
    
    return '[' + ','.join(result) + ']'


def deserialize(data):
    """
    Deserialize a string to a binary tree using level-order traversal.
    
    Args:
        data: str - serialized tree in format '[val1,val2,null,val3,...]'
        
    Returns:
        TreeNode or None - the root of the reconstructed binary tree
    """
    if data == '[]':
        return None
    
    # Parse the input string
    values = data[1:-1].split(',')  # Remove '[' and ']', then split by ','
    
    if not values or values[0] == '':
        return None
    
    root = TreeNode(int(values[0]))
    queue = deque([root])
    i = 1
    
    while queue and i < len(values):
        node = queue.popleft()
        
        # Process left child
        if i < len(values):
            if values[i] != 'null':
                node.left = TreeNode(int(values[i]))
                queue.append(node.left)
            i += 1
        
        # Process right child
        if i < len(values):
            if values[i] != 'null':
                node.right = TreeNode(int(values[i]))
                queue.append(node.right)
            i += 1
    
    return root
