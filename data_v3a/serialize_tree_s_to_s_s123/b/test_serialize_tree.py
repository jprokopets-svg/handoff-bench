import pytest
from serialize_tree import TreeNode, serialize, deserialize


def trees_equal(t1, t2):
    """Helper to compare two trees structurally."""
    if t1 is None and t2 is None:
        return True
    if t1 is None or t2 is None:
        return False
    return t1.val == t2.val and trees_equal(t1.left, t2.left) and trees_equal(t1.right, t2.right)


# ── serialize tests ──────────────────────────────────────────────────────────

class TestSerialize:
    def test_none_tree(self):
        assert serialize(None) == ""

    def test_single_node(self):
        root = TreeNode(1)
        assert serialize(root) == "1"

    def test_complete_tree(self):
        #     1
        #    / \
        #   2   3
        root = TreeNode(1, TreeNode(2), TreeNode(3))
        assert serialize(root) == "1,2,3"

    def test_left_skewed(self):
        #   1
        #  /
        # 2
        #  \
        #   3  (right child of 2)
        root = TreeNode(1, TreeNode(2, None, TreeNode(3)))
        assert serialize(root) == "1,2,null,null,3"

    def test_full_three_levels(self):
        #        1
        #      /   \
        #     2     3
        #    / \   / \
        #   4   5 6   7
        root = TreeNode(1,
                        TreeNode(2, TreeNode(4), TreeNode(5)),
                        TreeNode(3, TreeNode(6), TreeNode(7)))
        assert serialize(root) == "1,2,3,4,5,6,7"

    def test_missing_left_child(self):
        #   1
        #    \
        #     2
        root = TreeNode(1, None, TreeNode(2))
        assert serialize(root) == "1,null,2"

    def test_negative_values(self):
        root = TreeNode(-1, TreeNode(-2), TreeNode(-3))
        assert serialize(root) == "-1,-2,-3"

    def test_large_values(self):
        root = TreeNode(1000, TreeNode(2000), TreeNode(3000))
        assert serialize(root) == "1000,2000,3000"


# ── deserialize tests ────────────────────────────────────────────────────────

class TestDeserialize:
    def test_empty_string(self):
        assert deserialize("") is None

    def test_single_node(self):
        root = deserialize("1")
        assert root is not None
        assert root.val == 1
        assert root.left is None
        assert root.right is None

    def test_complete_tree(self):
        root = deserialize("1,2,3")
        assert root.val == 1
        assert root.left.val == 2
        assert root.right.val == 3

    def test_missing_left_child(self):
        root = deserialize("1,null,2")
        assert root.val == 1
        assert root.left is None
        assert root.right.val == 2

    def test_left_skewed(self):
        root = deserialize("1,2,null,null,3")
        assert root.val == 1
        assert root.left.val == 2
        assert root.left.right.val == 3
        assert root.left.left is None

    def test_full_three_levels(self):
        root = deserialize("1,2,3,4,5,6,7")
        assert root.val == 1
        assert root.left.val == 2
        assert root.right.val == 3
        assert root.left.left.val == 4
        assert root.left.right.val == 5
        assert root.right.left.val == 6
        assert root.right.right.val == 7

    def test_null_root(self):
        assert deserialize("null") is None

    def test_negative_values(self):
        root = deserialize("-1,-2,-3")
        assert root.val == -1
        assert root.left.val == -2
        assert root.right.val == -3


# ── round-trip tests ─────────────────────────────────────────────────────────

class TestRoundTrip:
    def _roundtrip(self, root):
        return deserialize(serialize(root))

    def test_none(self):
        assert self._roundtrip(None) is None

    def test_single_node(self):
        root = TreeNode(42)
        result = self._roundtrip(root)
        assert trees_equal(root, result)

    def test_complete_tree(self):
        root = TreeNode(1, TreeNode(2), TreeNode(3))
        assert trees_equal(root, self._roundtrip(root))

    def test_left_skewed(self):
        root = TreeNode(1, TreeNode(2, TreeNode(3)))
        assert trees_equal(root, self._roundtrip(root))

    def test_right_skewed(self):
        root = TreeNode(1, None, TreeNode(2, None, TreeNode(3)))
        assert trees_equal(root, self._roundtrip(root))

    def test_full_three_levels(self):
        root = TreeNode(1,
                        TreeNode(2, TreeNode(4), TreeNode(5)),
                        TreeNode(3, TreeNode(6), TreeNode(7)))
        assert trees_equal(root, self._roundtrip(root))

    def test_sparse_tree(self):
        #       1
        #      / \
        #     2   3
        #      \
        #       4
        root = TreeNode(1, TreeNode(2, None, TreeNode(4)), TreeNode(3))
        assert trees_equal(root, self._roundtrip(root))

    def test_negative_values(self):
        root = TreeNode(-5, TreeNode(-3), TreeNode(-8))
        assert trees_equal(root, self._roundtrip(root))

    def test_serialize_deserialize_string_stability(self):
        """Serializing a deserialized string should yield the same string."""
        s = "1,2,3,null,null,4,5"
        assert serialize(deserialize(s)) == s
