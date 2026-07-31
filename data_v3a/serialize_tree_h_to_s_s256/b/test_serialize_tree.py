import pytest
from serialize_tree import TreeNode, serialize, deserialize


def trees_equal(t1, t2):
    """Helper to compare two trees for structural and value equality."""
    if t1 is None and t2 is None:
        return True
    if t1 is None or t2 is None:
        return False
    return t1.val == t2.val and trees_equal(t1.left, t2.left) and trees_equal(t1.right, t2.right)


# ── serialize ────────────────────────────────────────────────────────────────

def test_serialize_empty_tree():
    assert serialize(None) == ""

def test_serialize_single_node():
    assert serialize(TreeNode(1)) == "1"

def test_serialize_complete_tree():
    #       1
    #      / \
    #     2   3
    root = TreeNode(1, TreeNode(2), TreeNode(3))
    assert serialize(root) == "1,2,3"

def test_serialize_left_skewed():
    #   1
    #  /
    # 2
    #  \
    #   3  (right child of 2)
    root = TreeNode(1, TreeNode(2, None, TreeNode(3)))
    assert serialize(root) == "1,2,null,null,3"

def test_serialize_right_only():
    #   1
    #    \
    #     2
    root = TreeNode(1, None, TreeNode(2))
    assert serialize(root) == "1,null,2"

def test_serialize_deeper_tree():
    #         1
    #        / \
    #       2   3
    #      / \
    #     4   5
    root = TreeNode(1,
                    TreeNode(2, TreeNode(4), TreeNode(5)),
                    TreeNode(3))
    assert serialize(root) == "1,2,3,4,5"

def test_serialize_negative_values():
    root = TreeNode(-1, TreeNode(-2), TreeNode(-3))
    assert serialize(root) == "-1,-2,-3"


# ── deserialize ──────────────────────────────────────────────────────────────

def test_deserialize_empty_string():
    assert deserialize("") is None

def test_deserialize_single_node():
    root = deserialize("1")
    assert root is not None
    assert root.val == 1
    assert root.left is None
    assert root.right is None

def test_deserialize_complete_tree():
    root = deserialize("1,2,3")
    assert root.val == 1
    assert root.left.val == 2
    assert root.right.val == 3

def test_deserialize_with_nulls():
    root = deserialize("1,null,2")
    assert root.val == 1
    assert root.left is None
    assert root.right.val == 2

def test_deserialize_deeper_nulls():
    root = deserialize("1,2,null,null,3")
    assert root.val == 1
    assert root.left.val == 2
    assert root.left.right.val == 3
    assert root.right is None


# ── round-trip ───────────────────────────────────────────────────────────────

def test_roundtrip_empty():
    assert deserialize(serialize(None)) is None

def test_roundtrip_single():
    original = TreeNode(42)
    result = deserialize(serialize(original))
    assert trees_equal(original, result)

def test_roundtrip_complete():
    original = TreeNode(1, TreeNode(2), TreeNode(3))
    result = deserialize(serialize(original))
    assert trees_equal(original, result)

def test_roundtrip_unbalanced():
    original = TreeNode(1,
                        TreeNode(2, TreeNode(4), TreeNode(5)),
                        TreeNode(3, None, TreeNode(6)))
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

def test_roundtrip_negative_values():
    original = TreeNode(-5, TreeNode(-3), TreeNode(-7))
    result = deserialize(serialize(original))
    assert trees_equal(original, result)

def test_serialize_idempotent():
    """serialize → deserialize → serialize should produce identical strings."""
    original = TreeNode(1,
                        TreeNode(2, TreeNode(4), TreeNode(5)),
                        TreeNode(3, None, TreeNode(6)))
    s1 = serialize(original)
    s2 = serialize(deserialize(s1))
    assert s1 == s2
