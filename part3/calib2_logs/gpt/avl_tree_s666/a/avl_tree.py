class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

class AVLTree:
    def __init__(self):
        self.root = None

    def contains(self, key: int) -> bool:
        n = self.root
        while n is not None:
            if key == n.val:
                return True
            elif key < n.val:
                n = n.left
            else:
                n = n.right
        return False

    def insert(self, key: int):
        def height(n):
            return 0 if n is None else 1 + max(height(n.left), height(n.right))

        def rotate_right(y):
            x = y.left
            T2 = x.right
            x.right = y
            y.left = T2
            return x

        def rotate_left(x):
            y = x.right
            T2 = y.left
            y.left = x
            x.right = T2
            return y

        def rebalance(node):
            if node is None:
                return node
            hl = height(node.left)
            hr = height(node.right)
            if hl - hr > 1:
                # left heavy
                if height(node.left.left) >= height(node.left.right):
                    # LL
                    node = rotate_right(node)
                else:
                    # LR
                    node.left = rotate_left(node.left)
                    node = rotate_right(node)
            elif hr - hl > 1:
                # right heavy
                if height(node.right.right) >= height(node.right.left):
                    # RR
                    node = rotate_left(node)
                else:
                    # RL
                    node.right = rotate_right(node.right)
                    node = rotate_left(node)
            return node

        def _insert(node, key):
            if node is None:
                return Node(key)
            if key == node.val:
                return node
            elif key < node.val:
                node.left = _insert(node.left, key)
            else:
                node.right = _insert(node.right, key)
            # rebalance
            node = rebalance(node)
            return node

        self.root = _insert(self.root, key)
        return None

    def delete(self, key: int):
        def height(n):
            return 0 if n is None else 1 + max(height(n.left), height(n.right))

        def rotate_right(y):
            x = y.left
            T2 = x.right
            x.right = y
            y.left = T2
            return x

        def rotate_left(x):
            y = x.right
            T2 = y.left
            y.left = x
            x.right = T2
            return y

        def rebalance(node):
            if node is None:
                return node
            hl = height(node.left)
            hr = height(node.right)
            if hl - hr > 1:
                if height(node.left.left) >= height(node.left.right):
                    node = rotate_right(node)
                else:
                    node.left = rotate_left(node.left)
                    node = rotate_right(node)
            elif hr - hl > 1:
                if height(node.right.right) >= height(node.right.left):
                    node = rotate_left(node)
                else:
                    node.right = rotate_right(node.right)
                    node = rotate_left(node)
            return node

        def find_min(node):
            while node.left is not None:
                node = node.left
            return node

        def _delete(node, key):
            if node is None:
                return None
            if key < node.val:
                node.left = _delete(node.left, key)
            elif key > node.val:
                node.right = _delete(node.right, key)
            else:
                # node to be deleted
                if node.left is None:
                    return node.right
                elif node.right is None:
                    return node.left
                else:
                    succ = find_min(node.right)
                    node.val = succ.val
                    node.right = _delete(node.right, succ.val)
            node = rebalance(node)
            return node

        self.root = _delete(self.root, key)
        return None
