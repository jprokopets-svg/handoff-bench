class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def get_height(self, node):
        return 0 if node is None else node.height

    def update_height(self, node):
        if node is not None:
            node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    def get_balance(self, node):
        if node is None:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def right_rotate(self, y):
        x = y.left
        T2 = x.right
        # rotation
        x.right = y
        y.left = T2
        # update heights
        self.update_height(y)
        self.update_height(x)
        return x

    def left_rotate(self, x):
        y = x.right
        T2 = y.left
        # rotation
        y.left = x
        x.right = T2
        # update heights
        self.update_height(x)
        self.update_height(y)
        return y

    def _insert(self, node, key):
        if node is None:
            return Node(key)
        if key == node.val:
            return node
        elif key < node.val:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)

        self.update_height(node)
        balance = self.get_balance(node)

        # Left Left
        if balance > 1 and key < node.left.val:
            return self.right_rotate(node)
        # Right Right
        if balance < -1 and key > node.right.val:
            return self.left_rotate(node)
        # Left Right
        if balance > 1 and key > node.left.val:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        # Right Left
        if balance < -1 and key < node.right.val:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def insert(self, key: int):
        self.root = self._insert(self.root, key)
        return None

    def contains(self, key: int) -> bool:
        node = self.root
        while node is not None:
            if key == node.val:
                return True
            elif key < node.val:
                node = node.left
            else:
                node = node.right
        return False

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def _delete(self, node, key):
        if node is None:
            return node
        if key < node.val:
            node.left = self._delete(node.left, key)
        elif key > node.val:
            node.right = self._delete(node.right, key)
        else:
            # node to be deleted
            if node.left is None:
                temp = node.right
                node = None
                return temp
            elif node.right is None:
                temp = node.left
                node = None
                return temp
            else:
                temp = self._min_value_node(node.right)
                node.val = temp.val
                node.right = self._delete(node.right, temp.val)

        # If the tree had only one node
        if node is None:
            return node

        # update height and rebalance
        self.update_height(node)
        balance = self.get_balance(node)

        # Left Left
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.right_rotate(node)
        # Left Right
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        # Right Right
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.left_rotate(node)
        # Right Left
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def delete(self, key: int):
        self.root = self._delete(self.root, key)
        return None
