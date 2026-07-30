from max_path_sum import TreeNode, max_path_sum


def test_case_1():
    n = TreeNode(1, TreeNode(2), TreeNode(3))
    assert max_path_sum(n) == 6


def test_case_2():
    n = TreeNode(-10, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
    assert max_path_sum(n) == 42


def test_case_3():
    n = TreeNode(-3)
    assert max_path_sum(n) == -3
