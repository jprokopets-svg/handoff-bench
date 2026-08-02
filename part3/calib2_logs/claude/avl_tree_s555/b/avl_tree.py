class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None

    def _height(self, node):
        """Get the height of a node."""
        return 0 if node is None else node.height

    def _balance_factor(self, node):
        """Calculate balance factor of a node."""
        if node is None:
            return 0
        return self._height(node.left) - self._height(node.right)

    def _update_height(self, node):
        """Update the height of a node based on its children."""
        if node is not None:
            node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _rotate_right(self, node):
        """Perform a right rotation."""
        left_child = node.left
        node.left = left_child.right
        left_child.right = node
        self._update_height(node)
        self._update_height(left_child)
        return left_child

    def _rotate_left(self, node):
        """Perform a left rotation."""
        right_child = node.right
        node.right = right_child.left
        right_child.left = node
        self._update_height(node)
        self._update_height(right_child)
        return right_child

    def _rebalance(self, node):
        """Rebalance a node using rotations if needed."""
        if node is None:
            return None

        self._update_height(node)
        balance = self._balance_factor(node)

        # Left heavy
        if balance > 1:
            # Left-Right case
            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)
            # Left-Left case
            return self._rotate_right(node)

        # Right heavy
        if balance < -1:
            # Right-Left case
            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)
            # Right-Right case
            return self._rotate_left(node)

        return node

    def insert(self, key: int) -> None:
        """Insert a key into the AVL tree."""
        self.root = self._insert_recursive(self.root, key)

    def _insert_recursive(self, node, key):
        """Recursively insert a key and rebalance."""
        if node is None:
            return Node(key)

        if key < node.val:
            node.left = self._insert_recursive(node.left, key)
        elif key > node.val:
            node.right = self._insert_recursive(node.right, key)
        else:
            # Duplicate key - no-op
            return node

        return self._rebalance(node)

    def delete(self, key: int) -> None:
        """Delete a key from the AVL tree."""
        self.root = self._delete_recursive(self.root, key)

    def _delete_recursive(self, node, key):
        """Recursively delete a key and rebalance."""
        if node is None:
            return None

        if key < node.val:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.val:
            node.right = self._delete_recursive(node.right, key)
        else:
            # Found the node to delete
            # Case 1: Node is a leaf
            if node.left is None and node.right is None:
                return None

            # Case 2: Node has only one child
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left

            # Case 3: Node has two children
            # Find the in-order successor (smallest node in right subtree)
            successor = self._find_min(node.right)
            node.val = successor.val
            node.right = self._delete_recursive(node.right, successor.val)

        return self._rebalance(node)

    def _find_min(self, node):
        """Find the node with minimum value in a subtree."""
        current = node
        while current.left is not None:
            current = current.left
        return current

    def contains(self, key: int) -> bool:
        """Check if a key exists in the AVL tree."""
        return self._contains_recursive(self.root, key)

    def _contains_recursive(self, node, key):
        """Recursively search for a key."""
        if node is None:
            return False

        if key == node.val:
            return True
        elif key < node.val:
            return self._contains_recursive(node.left, key)
        else:
            return self._contains_recursive(node.right, key)
