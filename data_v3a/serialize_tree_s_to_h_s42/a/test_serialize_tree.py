import pytest
from serialize_tree import TreeNode, serialize, deserialize


def trees_equal(t1, t2):
    """Helper to compare two binary trees for structural and value equality."""
    if t1 is None and t2 is None:
        return True
    if t1 is None or t2 is None:
        return False
    return t1.val == t2.val and trees_equal(t1.left, t2.left) and trees_equal(t1.right, t2.right)


# ── serialize ────────────────────────────────────────────────────────────────

class TestSerialize:
    def test_empty_tree(self):
        assert serialize(None) == ""

    def test_single_node(self):
        assert serialize(TreeNode(1)) == "1"

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
        # |
        # 3
        root = TreeNode(1, TreeNode(2, TreeNode(3)))
        assert serialize(root) == "1,2,null,3"

    def test_right_skewed(self):
        # 1
        #  \
        #   2
        #    \
        #     3
        root = TreeNode(1, None, TreeNode(2, None, TreeNode(3)))
        assert serialize(root) == "1,null,2,null,3"

    def test_mixed_tree(self):
        #       1
        #      / \
        #     2   3
        #    /   / \
        #   4   5   6
        root = TreeNode(1,
                        TreeNode(2, TreeNode(4)),
                        TreeNode(3, TreeNode(5), TreeNode(6)))
        assert serialize(root) == "1,2,3,4,null,5,6"

    def test_negative_values(self):
        root = TreeNode(-1, TreeNode(-2), TreeNode(-3))
        assert serialize(root) == "-1,-2,-3"

    def test_zero_value(self):
        root = TreeNode(0)
        assert serialize(root) == "0"


# ── deserialize ──────────────────────────────────────────────────────────────

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

    def test_left_skewed(self):
        root = deserialize("1,2,null,3")
        assert root.val == 1
        assert root.left.val == 2
        assert root.right is None
        assert root.left.left.val == 3

    def test_right_skewed(self):
        root = deserialize("1,null,2,null,3")
        assert root.val == 1
        assert root.left is None
        assert root.right.val == 2
        assert root.right.right.val == 3

    def test_mixed_tree(self):
        root = deserialize("1,2,3,4,null,5,6")
        assert root.val == 1
        assert root.left.val == 2
        assert root.right.val == 3
        assert root.left.left.val == 4
        assert root.left.right is None
        assert root.right.left.val == 5
        assert root.right.right.val == 6

    def test_negative_values(self):
        root = deserialize("-1,-2,-3")
        assert root.val == -1
        assert root.left.val == -2
        assert root.right.val == -3

    def test_null_root(self):
        assert deserialize("null") is None


# ── round-trip ───────────────────────────────────────────────────────────────

class TestRoundTrip:
    def _round_trip(self, root):
        return deserialize(serialize(root))

    def test_none(self):
        assert self._round_trip(None) is None

    def test_single_node(self):
        root = TreeNode(42)
        result = self._round_trip(root)
        assert trees_equal(root, result)

    def test_complete_tree(self):
        root = TreeNode(1, TreeNode(2), TreeNode(3))
        assert trees_equal(root, self._round_trip(root))

    def test_left_skewed(self):
        root = TreeNode(1, TreeNode(2, TreeNode(3)))
        assert trees_equal(root, self._round_trip(root))

    def test_right_skewed(self):
        root = TreeNode(1, None, TreeNode(2, None, TreeNode(3)))
        assert trees_equal(root, self._round_trip(root))

    def test_mixed_tree(self):
        root = TreeNode(1,
                        TreeNode(2, TreeNode(4)),
                        TreeNode(3, TreeNode(5), TreeNode(6)))
        assert trees_equal(root, self._round_trip(root))

    def test_large_tree(self):
        # Build a perfect binary tree of depth 4 (15 nodes)
        def build(val, depth):
            if depth == 0:
                return None
            return TreeNode(val, build(val * 2, depth - 1), build(val * 2 + 1, depth - 1))
        root = build(1, 4)
        assert trees_equal(root, self._round_trip(root))

    def test_negative_values(self):
        root = TreeNode(-5, TreeNode(-3), TreeNode(-8))
        assert trees_equal(root, self._round_trip(root))
