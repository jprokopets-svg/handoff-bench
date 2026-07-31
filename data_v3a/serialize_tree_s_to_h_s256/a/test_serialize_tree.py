import pytest
from serialize_tree import TreeNode, serialize, deserialize, trees_are_equal


# ── helpers ──────────────────────────────────────────────────────────────────

def build_tree(values):
    """Build a binary tree from a level-order list (None = missing node)."""
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


# ── serialize tests ───────────────────────────────────────────────────────────

class TestSerialize:

    def test_serialize_none(self):
        assert serialize(None) == "null"

    def test_serialize_single_node(self):
        root = TreeNode(1)
        assert serialize(root) == "1"

    def test_serialize_two_levels(self):
        #     1
        #    / \
        #   2   3
        root = TreeNode(1, TreeNode(2), TreeNode(3))
        assert serialize(root) == "1,2,3"

    def test_serialize_left_skewed(self):
        #   1
        #  /
        # 2
        #  \
        #   3  (right child of 2)
        root = TreeNode(1, TreeNode(2, None, TreeNode(3)))
        result = serialize(root)
        assert result == "1,2,null,null,3"

    def test_serialize_example_tree(self):
        #       1
        #      / \
        #     2   3
        #        / \
        #       4   5
        root = build_tree([1, 2, 3, None, None, 4, 5])
        result = serialize(root)
        assert result == "1,2,3,null,null,4,5"

    def test_serialize_complete_tree(self):
        #       1
        #      / \
        #     2   3
        #    / \ / \
        #   4  5 6  7
        root = build_tree([1, 2, 3, 4, 5, 6, 7])
        assert serialize(root) == "1,2,3,4,5,6,7"

    def test_serialize_negative_values(self):
        root = TreeNode(-1, TreeNode(-2), TreeNode(-3))
        assert serialize(root) == "-1,-2,-3"


# ── deserialize tests ─────────────────────────────────────────────────────────

class TestDeserialize:

    def test_deserialize_null(self):
        assert deserialize("null") is None

    def test_deserialize_empty_string(self):
        assert deserialize("") is None

    def test_deserialize_single_node(self):
        root = deserialize("1")
        assert root is not None
        assert root.val == 1
        assert root.left is None
        assert root.right is None

    def test_deserialize_two_levels(self):
        root = deserialize("1,2,3")
        assert root.val == 1
        assert root.left.val == 2
        assert root.right.val == 3

    def test_deserialize_with_nulls(self):
        root = deserialize("1,2,null,null,3")
        assert root.val == 1
        assert root.left.val == 2
        assert root.right is None
        assert root.left.left is None
        assert root.left.right.val == 3

    def test_deserialize_example_tree(self):
        root = deserialize("1,2,3,null,null,4,5")
        assert root.val == 1
        assert root.left.val == 2
        assert root.right.val == 3
        assert root.left.left is None
        assert root.left.right is None
        assert root.right.left.val == 4
        assert root.right.right.val == 5

    def test_deserialize_negative_values(self):
        root = deserialize("-1,-2,-3")
        assert root.val == -1
        assert root.left.val == -2
        assert root.right.val == -3


# ── round-trip tests ──────────────────────────────────────────────────────────

class TestRoundTrip:

    def _round_trip(self, root):
        return deserialize(serialize(root))

    def test_roundtrip_none(self):
        assert self._round_trip(None) is None

    def test_roundtrip_single_node(self):
        root = TreeNode(42)
        result = self._round_trip(root)
        assert trees_are_equal(root, result)

    def test_roundtrip_two_levels(self):
        root = TreeNode(1, TreeNode(2), TreeNode(3))
        assert trees_are_equal(root, self._round_trip(root))

    def test_roundtrip_example_tree(self):
        root = build_tree([1, 2, 3, None, None, 4, 5])
        assert trees_are_equal(root, self._round_trip(root))

    def test_roundtrip_left_only(self):
        root = build_tree([1, 2, None, 4, None])
        assert trees_are_equal(root, self._round_trip(root))

    def test_roundtrip_right_only(self):
        root = build_tree([1, None, 3, None, None, None, 5])
        assert trees_are_equal(root, self._round_trip(root))

    def test_roundtrip_complete_tree(self):
        root = build_tree([1, 2, 3, 4, 5, 6, 7])
        assert trees_are_equal(root, self._round_trip(root))

    def test_roundtrip_negative_values(self):
        root = TreeNode(-1, TreeNode(-2), TreeNode(-3))
        assert trees_are_equal(root, self._round_trip(root))

    def test_roundtrip_deep_tree(self):
        # Build a right-skewed tree: 1 -> 2 -> 3 -> 4 -> 5
        root = TreeNode(1)
        cur = root
        for v in range(2, 6):
            cur.right = TreeNode(v)
            cur = cur.right
        assert trees_are_equal(root, self._round_trip(root))

    def test_roundtrip_large_values(self):
        root = TreeNode(1000, TreeNode(999), TreeNode(1001))
        assert trees_are_equal(root, self._round_trip(root))


# ── trees_are_equal helper tests ──────────────────────────────────────────────

class TestTreesAreEqual:

    def test_both_none(self):
        assert trees_are_equal(None, None) is True

    def test_one_none(self):
        assert trees_are_equal(TreeNode(1), None) is False
        assert trees_are_equal(None, TreeNode(1)) is False

    def test_different_values(self):
        assert trees_are_equal(TreeNode(1), TreeNode(2)) is False

    def test_same_single_node(self):
        assert trees_are_equal(TreeNode(5), TreeNode(5)) is True

    def test_different_structure(self):
        t1 = TreeNode(1, TreeNode(2), None)
        t2 = TreeNode(1, None, TreeNode(2))
        assert trees_are_equal(t1, t2) is False
