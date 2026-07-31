import pytest
from serialize_tree import TreeNode, serialize, deserialize


def trees_equal(t1, t2):
    """Helper to compare two trees structurally."""
    if t1 is None and t2 is None:
        return True
    if t1 is None or t2 is None:
        return False
    return t1.val == t2.val and trees_equal(t1.left, t2.left) and trees_equal(t1.right, t2.right)


class TestSerialize:
    def test_serialize_none(self):
        assert serialize(None) == ""

    def test_serialize_single_node(self):
        root = TreeNode(1)
        assert serialize(root) == "1"

    def test_serialize_full_tree(self):
        #       1
        #      / \
        #     2   3
        #    / \ / \
        #   4  5 6  7
        root = TreeNode(1,
                        TreeNode(2, TreeNode(4), TreeNode(5)),
                        TreeNode(3, TreeNode(6), TreeNode(7)))
        assert serialize(root) == "1,2,3,4,5,6,7"

    def test_serialize_left_skewed(self):
        root = TreeNode(1, TreeNode(2, TreeNode(3)))
        assert serialize(root) == "1,2,null,3"

    def test_serialize_right_skewed(self):
        root = TreeNode(1, None, TreeNode(2, None, TreeNode(3)))
        assert serialize(root) == "1,null,2,null,3"

    def test_serialize_mixed(self):
        #     1
        #    / \
        #   2   3
        #      / \
        #     4   5
        root = TreeNode(1, TreeNode(2), TreeNode(3, TreeNode(4), TreeNode(5)))
        assert serialize(root) == "1,2,3,null,null,4,5"

    def test_serialize_negative_values(self):
        root = TreeNode(-1, TreeNode(-2), TreeNode(-3))
        assert serialize(root) == "-1,-2,-3"

    def test_serialize_large_values(self):
        root = TreeNode(1000, TreeNode(2000), TreeNode(3000))
        assert serialize(root) == "1000,2000,3000"


class TestDeserialize:
    def test_deserialize_empty(self):
        assert deserialize("") is None

    def test_deserialize_single_node(self):
        root = deserialize("1")
        assert root is not None
        assert root.val == 1
        assert root.left is None
        assert root.right is None

    def test_deserialize_full_tree(self):
        root = deserialize("1,2,3,4,5,6,7")
        assert root.val == 1
        assert root.left.val == 2
        assert root.right.val == 3
        assert root.left.left.val == 4
        assert root.left.right.val == 5
        assert root.right.left.val == 6
        assert root.right.right.val == 7

    def test_deserialize_left_skewed(self):
        root = deserialize("1,2,null,3")
        assert root.val == 1
        assert root.left.val == 2
        assert root.right is None
        assert root.left.left.val == 3

    def test_deserialize_right_skewed(self):
        root = deserialize("1,null,2,null,3")
        assert root.val == 1
        assert root.left is None
        assert root.right.val == 2
        assert root.right.right.val == 3

    def test_deserialize_mixed(self):
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


class TestRoundTrip:
    def _roundtrip(self, root):
        return deserialize(serialize(root))

    def test_roundtrip_none(self):
        assert self._roundtrip(None) is None

    def test_roundtrip_single_node(self):
        root = TreeNode(42)
        result = self._roundtrip(root)
        assert trees_equal(root, result)

    def test_roundtrip_full_tree(self):
        root = TreeNode(1,
                        TreeNode(2, TreeNode(4), TreeNode(5)),
                        TreeNode(3, TreeNode(6), TreeNode(7)))
        assert trees_equal(root, self._roundtrip(root))

    def test_roundtrip_left_skewed(self):
        root = TreeNode(1, TreeNode(2, TreeNode(3, TreeNode(4))))
        assert trees_equal(root, self._roundtrip(root))

    def test_roundtrip_right_skewed(self):
        root = TreeNode(1, None, TreeNode(2, None, TreeNode(3, None, TreeNode(4))))
        assert trees_equal(root, self._roundtrip(root))

    def test_roundtrip_mixed(self):
        root = TreeNode(1, TreeNode(2), TreeNode(3, TreeNode(4), TreeNode(5)))
        assert trees_equal(root, self._roundtrip(root))

    def test_roundtrip_negative_values(self):
        root = TreeNode(-10, TreeNode(-20, None, TreeNode(-30)), TreeNode(-5))
        assert trees_equal(root, self._roundtrip(root))

    def test_roundtrip_zero_value(self):
        root = TreeNode(0, TreeNode(0), TreeNode(0))
        assert trees_equal(root, self._roundtrip(root))
