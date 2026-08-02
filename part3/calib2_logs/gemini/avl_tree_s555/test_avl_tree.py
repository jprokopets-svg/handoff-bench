from avl_tree import *


def _h(n):
    return 0 if n is None else 1 + max(_h(n.left), _h(n.right))

def _bal(t):
    def walk(n):
        if n is None:
            return True
        if abs(_h(n.left) - _h(n.right)) > 1:
            return False
        return walk(n.left) and walk(n.right)
    return walk(t.root)

def _sorted_keys(t):
    out = []
    def walk(n):
        if n is None:
            return
        walk(n.left); out.append(n.val); walk(n.right)
    walk(t.root); return out

t = AVLTree();
for k in range(1, 101):
    t.insert(k)
    assert _bal(t)
assert _sorted_keys(t) == list(range(1, 101))

t = AVLTree();
for k in range(100, 0, -1):
    t.insert(k)
    assert _bal(t)
assert t.contains(1) and t.contains(100) and not t.contains(101)

t = AVLTree();
for k in [7, 3, 11, 1, 5, 9, 13, 0, 2, 4, 6, 8, 10, 12, 14]:
    t.insert(k)
assert _bal(t)
assert _sorted_keys(t) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

t = AVLTree();
for k in range(1, 21):
    t.insert(k)
for k in [10, 5, 1, 20, 15, 7, 13]:
    t.delete(k)
    assert _bal(t)
assert _sorted_keys(t) == [2, 3, 4, 6, 8, 9, 11, 12, 14, 16, 17, 18, 19]

t = AVLTree(); t.insert(5); t.insert(5); assert _sorted_keys(t) == [5]; t.delete(5); assert t.root is None and not t.contains(5)

t = AVLTree(); t.delete(9); assert t.root is None