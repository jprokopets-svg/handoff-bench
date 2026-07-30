from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Codec:
    def serialize(self, root):
        """Encodes a tree to a single string using level-order traversal."""
        if not root:
            return ""
        
        result = []
        queue = deque([root])
        
        while queue:
            node = queue.popleft()
            if node:
                result.append(str(node.val))
                queue.append(node.left)
                queue.append(node.right)
            else:
                result.append("null")
        
        return ",".join(result)
    
    def deserialize(self, data):
        """Decodes your encoded data to tree."""
        if not data:
            return None
        
        values = data.split(",")
        root = TreeNode(int(values[0]))
        queue = deque([root])
        i = 1
        
        while queue and i < len(values):
            node = queue.popleft()
            
            # Process left child
            if i < len(values):
                if values[i] != "null":
                    node.left = TreeNode(int(values[i]))
                    queue.append(node.left)
                i += 1
            
            # Process right child
            if i < len(values):
                if values[i] != "null":
                    node.right = TreeNode(int(values[i]))
                    queue.append(node.right)
                i += 1
        
        return root
