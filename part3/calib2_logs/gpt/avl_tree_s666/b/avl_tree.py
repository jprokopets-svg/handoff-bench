class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1  # height of subtree rooted at this node (leaf = 1)

class AVLTree:
    def __init__(self):
        self.root = None

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

    def insert(self, key: int) -> None:
        def get_height(n):
            return n.height if n is not None else 0

        def update_height(n):
            n.height = 1 + max(get_height(n.left), get_height(n.right))

        def rotate_right(y):
            x = y.left
            T2 = x.right
            # rotation
            x.right = y
            y.left = T2
            # update heights
            update_height(y)
            update_height(x)
            return x

        def rotate_left(x):
            y = x.right
            T2 = y.left
            # rotation
            y.left = x
            x.right = T2
            # update heights
            update_height(x)
            update_height(y)
            return y

        def get_balance(n):
            return 0 if n is None else get_height(n.left) - get_height(n.right)

        def _insert(node, key):
            if node is None:
                return Node(key)
            if key == node.val:
                return node  # ignore duplicates
            elif key < node.val:
                node.left = _insert(node.left, key)
            else:
                node.right = _insert(node.right, key)

            update_height(node)
            balance = get_balance(node)

            # Left heavy
            if balance > 1:
                if key < node.left.val:
                    # Left Left
                    return rotate_right(node)
                else:
                    # Left Right
                    node.left = rotate_left(node.left)
                    return rotate_right(node)
            # Right heavy
            if balance < -1:
                if key > node.right.val:
                    # Right Right
                    return rotate_left(node)
                else:
                    # Right Left
                    node.right = rotate_right(node.right)
                    return rotate_left(node)

            return node

        self.root = _insert(self.root, key)
        return None

    def delete(self, key: int) -> None:
        def get_height(n):
            return n.height if n is not None else 0

        def update_height(n):
            n.height = 1 + max(get_height(n.left), get_height(n.right))

        def rotate_right(y):
            x = y.left
            T2 = x.right
            x.right = y
            y.left = T2
            update_height(y)
            update_height(x)
            return x

        def rotate_left(x):
            y = x.right
            T2 = y.left
            y.left = x
            x.right = T2
            update_height(x)
            update_height(y)
            return y

        def get_balance(n):
            return 0 if n is None else get_height(n.left) - get_height(n.right)

        def min_value_node(n):
            cur = n
            while cur.left is not None:
                cur = cur.left
            return cur

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
                    # two children: get inorder successor (smallest in right subtree)
                    temp = min_value_node(node.right)
                    node.val = temp.val
                    node.right = _delete(node.right, temp.val)

            # if we reached here node might be None after deletion of child
            if node is None:
                return None

            update_height(node)
            balance = get_balance(node)

            # Left heavy
            if balance > 1:
                # Left Left
                if get_balance(node.left) >= 0:
                    return rotate_right(node)
                else:
                    node.left = rotate_left(node.left)
                    return rotate_right(node)
            # Right heavy
            if balance < -1:
                # Right Right
                if get_balance(node.right) <= 0:
                    return rotate_left(node)
                else:
                    node.right = rotate_right(node.right)
                    return rotate_left(node)

            return node

        self.root = _delete(self.root, key)
        return None
