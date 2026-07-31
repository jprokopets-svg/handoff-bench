import pytest
from serialize_tree import TreeNode, serialize, deserialize


def make_tree(values):
    """Helper to build a tree from a list (level-order, None for missing nodes)."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    from collections import deque
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root


def trees_equal(t1, t2):
    if t1 is None and t2 is None:
        return True
    if t1 is None or t2 is None:
        return False
    return t1.val == t2.val and trees_equal(t1.left, t2.left) and trees_equal(t1.right, t2.right)


# --- serialize tests ---

def test_serialize_none():
    assert serialize(None) == ""

def test_serialize_single_node():
    root = TreeNode(1)
    assert serialize(root) == "1"

def test_serialize_two_levels():
    root = TreeNode(1, TreeNode(2), TreeNode(3))
    assert serialize(root) == "1,2,3"

def test_serialize_with_nulls():
    # Tree:   1
    #        / \
    #       2   3
    #          / \
    #         4   5
    root = TreeNode(1, TreeNode(2), TreeNode(3, TreeNode(4), TreeNode(5)))
    assert serialize(root) == "1,2,3,null,null,4,5"

def test_serialize_left_skewed():
    root = TreeNode(1, TreeNode(2, TreeNode(3)))
    assert serialize(root) == "1,2,null,3"

def test_serialize_right_skewed():
    root = TreeNode(1, None, TreeNode(2, None, TreeNode(3)))
    assert serialize(root) == "1,null,2,null,3"

def test_serialize_negative_values():
    root = TreeNode(-1, TreeNode(-2), TreeNode(-3))
    assert serialize(root) == "-1,-2,-3"


# --- deserialize tests ---

def test_deserialize_empty():
    assert deserialize("") is None

def test_deserialize_single_node():
    root = deserialize("1")
    assert root is not None
    assert root.val == 1
    assert root.left is None
    assert root.right is None

def test_deserialize_two_levels():
    root = deserialize("1,2,3")
    assert root.val == 1
    assert root.left.val == 2
    assert root.right.val == 3

def test_deserialize_with_nulls():
    root = deserialize("1,2,3,null,null,4,5")
    assert root.val == 1
    assert root.left.val == 2
    assert root.right.val == 3
    assert root.left.left is None
    assert root.left.right is None
    assert root.right.left.val == 4
    assert root.right.right.val == 5

def test_deserialize_left_skewed():
    root = deserialize("1,2,null,3")
    assert root.val == 1
    assert root.left.val == 2
    assert root.right is None
    assert root.left.left.val == 3

def test_deserialize_right_skewed():
    root = deserialize("1,null,2,null,3")
    assert root.val == 1
    assert root.left is None
    assert root.right.val == 2
    assert root.right.right.val == 3

def test_deserialize_negative_values():
    root = deserialize("-1,-2,-3")
    assert root.val == -1
    assert root.left.val == -2
    assert root.right.val == -3


# --- round-trip tests ---

def test_roundtrip_none():
    assert deserialize(serialize(None)) is None

def test_roundtrip_single():
    original = TreeNode(42)
    result = deserialize(serialize(original))
    assert trees_equal(original, result)

def test_roundtrip_full_tree():
    original = TreeNode(1, TreeNode(2), TreeNode(3, TreeNode(4), TreeNode(5)))
    result = deserialize(serialize(original))
    assert trees_equal(original, result)

def test_roundtrip_left_skewed():
    original = TreeNode(1, TreeNode(2, TreeNode(3, TreeNode(4))))
    result = deserialize(serialize(original))
    assert trees_equal(original, result)

def test_roundtrip_right_skewed():
    original = TreeNode(1, None, TreeNode(2, None, TreeNode(3, None, TreeNode(4))))
    result = deserialize(serialize(original))
    assert trees_equal(original, result)

def test_roundtrip_complex():
    #        5
    #       / \
    #      3   8
    #     / \   \
    #    1   4   9
    original = TreeNode(5,
        TreeNode(3, TreeNode(1), TreeNode(4)),
        TreeNode(8, None, TreeNode(9))
    )
    result = deserialize(serialize(original))
    assert trees_equal(original, result)

def test_roundtrip_large_values():
    original = TreeNode(1000, TreeNode(-999), TreeNode(500))
    result = deserialize(serialize(original))
    assert trees_equal(original, result)
