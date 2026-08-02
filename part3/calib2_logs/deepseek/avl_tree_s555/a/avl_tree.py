class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1  # height of node, leaf height = 1


class AVLTree:
    def __init__(self):
        self.root = None

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
        self._update_height(node)
        balance = self._balance_factor(node)

        # Left heavy
        if balance > 1:
            # Left-left case
            if self._balance_factor(node.left) >= 0:
                return self._rotate_right(node)
            # Left-right case
            else:
                node.left = self._rotate_left(node.left)
                return self._rotate_right(node)
        # Right heavy
        if balance < -1:
            # Right-right case
            if self._balance_factor(node.right) <= 0:
                return self._rotate_left(node)
            # Right-left case
            else:
                node.right = self._rotate_right(node.right)
                return self._rotate_left(node)
        return node

    def _insert_node(self, node, key):
        if not node:
            return Node(key)
        if key < node.val:
            node.left = self._insert_node(node.left, key)
        elif key > node.val:
            node.right = self._insert_node(node.right, key)
        else:
            # duplicate, do nothing
            return node
        return self._rebalance(node)

    def insert(self, key: int) -> None:
        self.root = self._insert_node(self.root, key)

    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def _delete_node(self, node, key):
        if not node:
            return None
        if key < node.val:
            node.left = self._delete_node(node.left, key)
        elif key > node.val:
            node.right = self._delete_node(node.right, key)
        else:
            # node to delete found
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            else:
                # node with two children
                temp = self._min_value_node(node.right)
                node.val = temp.val
                node.right = self._delete_node(node.right, temp.val)
        return self._rebalance(node)

    def delete(self, key: int) -> None:
        self.root = self._delete_node(self.root, key)

    def _contains_node(self, node, key):
        if not node:
            return False
        if key < node.val:
            return self._contains_node(node.left, key)
        elif key > node.val:
            return self._contains_node(node.right, key)
        else:
            return True

    def contains(self, key: int) -> bool:
        return self._contains_node(self.root, key)