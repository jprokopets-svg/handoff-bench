import pytest
from serialize_tree import TreeNode, serialize, deserialize, trees_are_equal


# ── helpers ──────────────────────────────────────────────────────────────────

def build_tree(values):
    """Build a tree from a level-order list (None = missing node)."""
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
    def test_none_tree(self):
        assert serialize(None) == "null"

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
        #  \
        #   3  (right child of 2)
        root = TreeNode(1, TreeNode(2, None, TreeNode(3)))
        result = serialize(root)
        # Must encode the missing left child of 2
        assert "null" in result
        assert result == "1,2,null,null,3"

    def test_right_skewed(self):
        root = TreeNode(1, None, TreeNode(2, None, TreeNode(3)))
        result = serialize(root)
        assert "null" in result

    def test_larger_tree(self):
        #       1
        #      / \
        #     2   3
        #        / \
        #       4   5
        root = build_tree([1, 2, 3, None, None, 4, 5])
        result = serialize(root)
        assert result == "1,2,3,null,null,4,5"

    def test_negative_values(self):
        root = TreeNode(-1, TreeNode(-2), TreeNode(-3))
        result = serialize(root)
        assert "-1" in result
        assert "-2" in result
        assert "-3" in result


# ── deserialize tests ─────────────────────────────────────────────────────────

class TestDeserialize:
    def test_null_string(self):
        assert deserialize("null") is None

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

    def test_tree_with_nulls(self):
        root = deserialize("1,2,3,null,null,4,5")
        assert root.val == 1
        assert root.left.val == 2
        assert root.right.val == 3
        assert root.left.left is None
        assert root.left.right is None
        assert root.right.left.val == 4
        assert root.right.right.val == 5

    def test_negative_values(self):
        root = deserialize("-1,-2,-3")
        assert root.val == -1
        assert root.left.val == -2
        assert root.right.val == -3


# ── round-trip tests ──────────────────────────────────────────────────────────

class TestRoundTrip:
    def _round_trip(self, root):
        return deserialize(serialize(root))

    def test_none(self):
        assert self._round_trip(None) is None

    def test_single_node(self):
        original = TreeNode(42)
        result = self._round_trip(original)
        assert trees_are_equal(original, result)

    def test_complete_tree(self):
        original = TreeNode(1, TreeNode(2), TreeNode(3))
        assert trees_are_equal(original, self._round_trip(original))

    def test_larger_tree(self):
        original = build_tree([1, 2, 3, None, None, 4, 5])
        assert trees_are_equal(original, self._round_trip(original))

    def test_left_skewed(self):
        original = build_tree([1, 2, None, 3, None, 4])
        assert trees_are_equal(original, self._round_trip(original))

    def test_right_skewed(self):
        original = build_tree([1, None, 2, None, 3, None, 4])
        assert trees_are_equal(original, self._round_trip(original))

    def test_negative_values(self):
        original = TreeNode(-1, TreeNode(-2), TreeNode(-3))
        assert trees_are_equal(original, self._round_trip(original))

    def test_deep_tree(self):
        # Build a deeper tree: 1->2->3->4->5 (left spine)
        original = build_tree([1, 2, None, 3, None, 4, None, 5])
        assert trees_are_equal(original, self._round_trip(original))

    def test_full_tree(self):
        original = build_tree([1, 2, 3, 4, 5, 6, 7])
        assert trees_are_equal(original, self._round_trip(original))
