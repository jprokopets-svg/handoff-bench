import pytest
from serialize_tree import TreeNode, serialize, deserialize


def make_tree(values):
    """Helper: build a tree from a level-order list (None = missing node)."""
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
    """Helper: convert tree back to level-order list (None = missing node)."""
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
    # Strip trailing Nones
    while result and result[-1] is None:
        result.pop()
    return result


# ---------------------------------------------------------------------------
# Tests for serialize
# ---------------------------------------------------------------------------

class TestSerialize:
    def test_empty_tree(self):
        assert serialize(None) == ""

    def test_single_node(self):
        root = TreeNode(1)
        assert serialize(root) == "1"

    def test_complete_tree(self):
        root = make_tree([1, 2, 3, 4, 5, 6, 7])
        assert serialize(root) == "1,2,3,4,5,6,7"

    def test_left_skewed(self):
        root = make_tree([1, 2, None, 3, None, None, None])
        assert serialize(root) == "1,2,null,3"

    def test_right_skewed(self):
        root = TreeNode(1)
        root.right = TreeNode(2)
        root.right.right = TreeNode(3)
        assert serialize(root) == "1,null,2,null,3"

    def test_tree_with_gap(self):
        # Tree: 1 -> right: 2
        root = TreeNode(1)
        root.right = TreeNode(2)
        assert serialize(root) == "1,null,2"

    def test_negative_values(self):
        root = TreeNode(-1)
        root.left = TreeNode(-2)
        root.right = TreeNode(-3)
        assert serialize(root) == "-1,-2,-3"

    def test_trailing_nulls_stripped(self):
        # A complete tree should have no trailing nulls
        root = make_tree([1, 2, 3])
        s = serialize(root)
        assert not s.endswith("null")


# ---------------------------------------------------------------------------
# Tests for deserialize
# ---------------------------------------------------------------------------

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

    def test_tree_with_gap(self):
        root = deserialize("1,null,2")
        assert root.val == 1
        assert root.left is None
        assert root.right.val == 2

    def test_negative_values(self):
        root = deserialize("-1,-2,-3")
        assert root.val == -1
        assert root.left.val == -2
        assert root.right.val == -3


# ---------------------------------------------------------------------------
# Round-trip tests (serialize → deserialize → serialize)
# ---------------------------------------------------------------------------

class TestRoundTrip:
    def _round_trip(self, root):
        return deserialize(serialize(root))

    def test_empty_tree(self):
        assert self._round_trip(None) is None

    def test_single_node(self):
        root = TreeNode(42)
        result = self._round_trip(root)
        assert result.val == 42
        assert result.left is None
        assert result.right is None

    def test_complete_tree(self):
        original = make_tree([1, 2, 3, 4, 5, 6, 7])
        result = self._round_trip(original)
        assert tree_to_list(result) == [1, 2, 3, 4, 5, 6, 7]

    def test_left_skewed(self):
        original = make_tree([1, 2, None, 3])
        result = self._round_trip(original)
        assert tree_to_list(result) == [1, 2, None, 3]

    def test_right_skewed(self):
        root = TreeNode(1)
        root.right = TreeNode(2)
        root.right.right = TreeNode(3)
        result = self._round_trip(root)
        assert tree_to_list(result) == [1, None, 2, None, 3]

    def test_tree_with_gap(self):
        root = TreeNode(1)
        root.right = TreeNode(2)
        result = self._round_trip(root)
        assert result.val == 1
        assert result.left is None
        assert result.right.val == 2

    def test_serialize_deserialize_string_match(self):
        """Serializing twice should produce the same string."""
        root = make_tree([1, 2, 3, 4, 5, 6, 7])
        s1 = serialize(root)
        s2 = serialize(deserialize(s1))
        assert s1 == s2

    def test_large_tree(self):
        """15-node complete binary tree."""
        vals = list(range(1, 16))
        original = make_tree(vals)
        result = self._round_trip(original)
        assert tree_to_list(result) == vals
