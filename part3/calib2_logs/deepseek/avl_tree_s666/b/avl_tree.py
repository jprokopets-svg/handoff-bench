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
        self.root = self._insert(self.root, key)

    def delete(self, key: int) -> None:
        self.root = self._delete(self.root, key)

    def contains(self, key: int) -> bool:
        return self._contains(self.root, key)

    # Helper methods
    def _height(self, node):
        return node.height if node else 0

    def _update_height(self, node):
        if node:
            node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _balance_factor(self, node):
        if not node:
            return 0
        return self._height(node.left) - self._height(node.right)

    def _rotate_right(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        self._update_height(y)
        self._update_height(x)

        return x

    def _rotate_left(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        self._update_height(x)
        self._update_height(y)

        return y

    def _rebalance(self, node):
        if not node:
            return node

        self._update_height(node)
        balance = self._balance_factor(node)

        # Left heavy
        if balance > 1:
            # Left-Right case
            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Right heavy
        if balance < -1:
            # Right-Left case
            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def _insert(self, node, key):
        if not node:
            return Node(key)

        if key < node.val:
            node.left = self._insert(node.left, key)
        elif key > node.val:
            node.right = self._insert(node.right, key)
        else:
            # Duplicate key, no-op
            return node

        return self._rebalance(node)

    def _contains(self, node, key):
        if not node:
            return False
        if key == node.val:
            return True
        elif key < node.val:
            return self._contains(node.left, key)
        else:
            return self._contains(node.right, key)

    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def _delete(self, node, key):
        if not node:
            return None

        if key < node.val:
            node.left = self._delete(node.left, key)
        elif key > node.val:
            node.right = self._delete(node.right, key)
        else:
            # Node to delete found
            # Node with only one child or no child
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            else:
                # Node with two children
                temp = self._min_value_node(node.right)
                node.val = temp.val
                node.right = self._delete(node.right, temp.val)

        return self._rebalance(node)