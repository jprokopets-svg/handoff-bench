import pytest
from serialize_tree import TreeNode, serialize, deserialize


# ── helpers ──────────────────────────────────────────────────────────────────

def build_tree(values):
    """Build a tree from a level-order list (None = missing node)."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    while queue and i < len(values):
        node = queue.pop(0)
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root


def tree_to_list(root):
    """Convert a tree back to a level-order list (None = missing node)."""
    if not root:
        return []
    result = []
    queue = [root]
    while queue:
        node = queue.pop(0)
        if node:
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            result.append(None)
    # strip trailing Nones
    while result and result[-1] is None:
        result.pop()
    return result


def trees_equal(t1, t2):
    """Recursively check structural + value equality."""
    if t1 is None and t2 is None:
        return True
    if t1 is None or t2 is None:
        return False
    return (t1.val == t2.val and
            trees_equal(t1.left, t2.left) and
            trees_equal(t1.right, t2.right))


# ── serialize tests ───────────────────────────────────────────────────────────

class TestSerialize:

    def test_empty_tree(self):
        assert serialize(None) == ""

    def test_single_node(self):
        root = TreeNode(1)
        assert serialize(root) == "1"

    def test_complete_tree(self):
        #       1
        #      / \
        #     2   3
        #    / \ / \
        #   4  5 6  7
        root = build_tree([1, 2, 3, 4, 5, 6, 7])
        assert serialize(root) == "1,2,3,4,5,6,7"

    def test_left_skewed(self):
        #   1
        #  /
        # 2
        #  \
        #   3  (right child of 2)
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.left.right = TreeNode(3)
        result = serialize(root)
        assert result == "1,2,null,null,3"

    def test_right_skewed(self):
        root = TreeNode(1)
        root.right = TreeNode(2)
        root.right.right = TreeNode(3)
        result = serialize(root)
        assert result == "1,null,2,null,3"

    def test_sparse_tree_with_nulls(self):
        #       1
        #      / \
        #     2   3
        #      \
        #       4
        root = build_tree([1, 2, 3, None, 4])
        result = serialize(root)
        assert result == "1,2,3,null,4"

    def test_negative_values(self):
        root = TreeNode(-1)
        root.left = TreeNode(-2)
        root.right = TreeNode(-3)
        result = serialize(root)
        assert result == "-1,-2,-3"

    def test_trailing_nulls_removed(self):
        #   1
        #  /
        # 2
        root = TreeNode(1)
        root.left = TreeNode(2)
        result = serialize(root)
        # Should NOT end with ",null"
        assert not result.endswith("null")
        assert result == "1,2"


# ── deserialize tests ─────────────────────────────────────────────────────────

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
        root = deserialize("1,2,3,4,5,6,7")
        assert tree_to_list(root) == [1, 2, 3, 4, 5, 6, 7]

    def test_left_skewed(self):
        root = deserialize("1,2,null,null,3")
        assert root.val == 1
        assert root.left.val == 2
        assert root.left.left is None
        assert root.left.right.val == 3
        assert root.right is None

    def test_right_skewed(self):
        root = deserialize("1,null,2,null,3")
        assert root.val == 1
        assert root.left is None
        assert root.right.val == 2
        assert root.right.right.val == 3

    def test_sparse_tree_with_nulls(self):
        root = deserialize("1,2,3,null,4")
        assert root.val == 1
        assert root.left.val == 2
        assert root.right.val == 3
        assert root.left.left is None
        assert root.left.right.val == 4

    def test_negative_values(self):
        root = deserialize("-1,-2,-3")
        assert root.val == -1
        assert root.left.val == -2
        assert root.right.val == -3


# ── round-trip tests ──────────────────────────────────────────────────────────

class TestRoundTrip:

    def _round_trip(self, root):
        return deserialize(serialize(root))

    def test_empty_tree(self):
        assert self._round_trip(None) is None

    def test_single_node(self):
        root = TreeNode(42)
        result = self._round_trip(root)
        assert trees_equal(root, result)

    def test_complete_tree(self):
        root = build_tree([1, 2, 3, 4, 5, 6, 7])
        assert trees_equal(root, self._round_trip(root))

    def test_left_only_tree(self):
        root = build_tree([1, 2, None, 3])
        assert trees_equal(root, self._round_trip(root))

    def test_right_only_tree(self):
        root = build_tree([1, None, 2, None, 3])
        assert trees_equal(root, self._round_trip(root))

    def test_sparse_tree(self):
        root = build_tree([1, 2, 3, None, 4, None, 5])
        assert trees_equal(root, self._round_trip(root))

    def test_deep_tree(self):
        # Build a chain: 1 -> 2 -> 3 -> ... -> 10 (all left children)
        root = TreeNode(1)
        cur = root
        for v in range(2, 11):
            cur.left = TreeNode(v)
            cur = cur.left
        assert trees_equal(root, self._round_trip(root))

    def test_large_complete_tree(self):
        root = build_tree(list(range(1, 32)))  # 31 nodes, 5 levels
        assert trees_equal(root, self._round_trip(root))

    def test_negative_values(self):
        root = build_tree([-5, -3, -1, -7, None, -2, None])
        assert trees_equal(root, self._round_trip(root))

    def test_zero_value_node(self):
        root = TreeNode(0)
        root.left = TreeNode(0)
        root.right = TreeNode(0)
        assert trees_equal(root, self._round_trip(root))
