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

    def get_balance(self, node):
        if node is None:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def right_rotate(self, y):
        x = y.left
        T2 = x.right
        # rotate
        x.right = y
        y.left = T2
        # update heights
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        return x

    def left_rotate(self, x):
        y = x.right
        T2 = y.left
        # rotate
        y.left = x
        x.right = T2
        # update heights
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def insert(self, key: int) -> None:
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        # normal BST insert
        if node is None:
            return Node(key)
        if key < node.val:
            node.left = self._insert(node.left, key)
        elif key > node.val:
            node.right = self._insert(node.right, key)
        else:
            # duplicate: no-op
            return node
        # update height
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        # rebalance
        balance = self.get_balance(node)
        # LL
        if balance > 1 and key < node.left.val:
            return self.right_rotate(node)
        # RR
        if balance < -1 and key > node.right.val:
            return self.left_rotate(node)
        # LR
        if balance > 1 and key > node.left.val:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        # RL
        if balance < -1 and key < node.right.val:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)
        return node

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def delete(self, key: int) -> None:
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if node is None:
            return None
        # BST delete
        if key < node.val:
            node.left = self._delete(node.left, key)
        elif key > node.val:
            node.right = self._delete(node.right, key)
        else:
            # node with one or no child
            if node.left is None:
                temp = node.right
                node = None
                return temp
            elif node.right is None:
                temp = node.left
                node = None
                return temp
            # node with two children: get inorder successor
            temp = self._min_value_node(node.right)
            node.val = temp.val
            node.right = self._delete(node.right, temp.val)
        # if the tree had only one node
        if node is None:
            return None
        # update height
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        # rebalance
        balance = self.get_balance(node)
        # Left heavy
        if balance > 1:
            # Left-Left
            if self.get_balance(node.left) >= 0:
                return self.right_rotate(node)
            # Left-Right
            else:
                node.left = self.left_rotate(node.left)
                return self.right_rotate(node)
        # Right heavy
        if balance < -1:
            # Right-Right
            if self.get_balance(node.right) <= 0:
                return self.left_rotate(node)
            # Right-Left
            else:
                node.right = self.right_rotate(node.right)
                return self.left_rotate(node)
        return node

    def contains(self, key: int) -> bool:
        cur = self.root
        while cur is not None:
            if key == cur.val:
                return True
            elif key < cur.val:
                cur = cur.left
            else:
                cur = cur.right
        return False
