class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, key: int) -> None:
        """Insert a key into the AVL tree. Duplicates are ignored."""
        self.root = self._insert_recursive(self.root, key)

    def _insert_recursive(self, node, key):
        if node is None:
            return Node(key)
        
        if key < node.val:
            node.left = self._insert_recursive(node.left, key)
        elif key > node.val:
            node.right = self._insert_recursive(node.right, key)
        else:
            # Duplicate - no-op
            return node
        
        # Update height and rebalance
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        return self._balance(node)

    def delete(self, key: int) -> None:
        """Delete a key from the AVL tree. Missing keys are ignored."""
        self.root = self._delete_recursive(self.root, key)

    def _delete_recursive(self, node, key):
        if node is None:
            return None
        
        if key < node.val:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.val:
            node.right = self._delete_recursive(node.right, key)
        else:
            # Node to delete found
            # Case 1: No children (leaf)
            if node.left is None and node.right is None:
                return None
            # Case 2: One child
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            # Case 3: Two children - find successor
            successor = self._find_min(node.right)
            node.val = successor.val
            node.right = self._delete_recursive(node.right, successor.val)
        
        if node is None:
            return None
        
        # Update height and rebalance
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        return self._balance(node)

    def contains(self, key: int) -> bool:
        """Check if a key exists in the AVL tree."""
        return self._contains_recursive(self.root, key)

    def _contains_recursive(self, node, key):
        if node is None:
            return False
        if key == node.val:
            return True
        elif key < node.val:
            return self._contains_recursive(node.left, key)
        else:
            return self._contains_recursive(node.right, key)

    def _get_height(self, node):
        """Get the height of a node."""
        return 0 if node is None else node.height

    def _get_balance(self, node):
        """Get the balance factor of a node."""
        if node is None:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _balance(self, node):
        """Rebalance the tree at this node."""
        balance = self._get_balance(node)
        
        # Left heavy
        if balance > 1:
            # Left-Right case
            if self._get_balance(node.left) < 0:
                node.left = self._rotate_left(node.left)
            # Left-Left case
            return self._rotate_right(node)
        
        # Right heavy
        if balance < -1:
            # Right-Left case
            if self._get_balance(node.right) > 0:
                node.right = self._rotate_right(node.right)
            # Right-Right case
            return self._rotate_left(node)
        
        return node

    def _rotate_left(self, node):
        """Perform a left rotation."""
        right_child = node.right
        node.right = right_child.left
        right_child.left = node
        
        # Update heights
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        right_child.height = 1 + max(self._get_height(right_child.left), self._get_height(right_child.right))
        
        return right_child

    def _rotate_right(self, node):
        """Perform a right rotation."""
        left_child = node.left
        node.left = left_child.right
        left_child.right = node
        
        # Update heights
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        left_child.height = 1 + max(self._get_height(left_child.left), self._get_height(left_child.right))
        
        return left_child

    def _find_min(self, node):
        """Find the node with minimum value in a subtree."""
        current = node
        while current.left is not None:
            current = current.left
        return current
