from max_path_sum import *


n = TreeNode(1, TreeNode(2), TreeNode(3)); assert max_path_sum(n) == 6

n = TreeNode(-10, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7))); assert max_path_sum(n) == 42

n = TreeNode(-3); assert max_path_sum(n) == -3