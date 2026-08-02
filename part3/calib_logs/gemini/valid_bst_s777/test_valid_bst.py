from valid_bst import *


n = TreeNode(2, TreeNode(1), TreeNode(3)); assert is_valid_bst(n) == True

n = TreeNode(5, TreeNode(1), TreeNode(4, TreeNode(3), TreeNode(6))); assert is_valid_bst(n) == False

n = TreeNode(2, TreeNode(2), TreeNode(2)); assert is_valid_bst(n) == False

assert is_valid_bst(None) == True

n = TreeNode(5, TreeNode(4), TreeNode(6, TreeNode(3), TreeNode(7))); assert is_valid_bst(n) == False