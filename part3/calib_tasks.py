#!/usr/bin/env python3
"""part3/calib_tasks.py — Handoff Part III hard-tier calibration candidates.

12 tasks, materially harder than V2 (multi-function, edge-case-dense, or
stateful). Disjoint from the V2 task set (regex_parser, n_queens, median_stream,
word_break, median_two_sorted, serialize_tree, max_path_sum, merge_k_lists) and
from the 5 Stage 0 tasks (two_sum, valid_palindrome, fibonacci, count_bits,
climbing_stairs). Per CALIBRATION_PREREG.md, candidates selected by pooled
20-80% success; selected tier becomes the confirmatory hard tier.
"""

CALIB_TASKS = [
    {
        "name": "atoi_clone",
        "prompt": "Write a function that converts a string to a 32-bit signed integer. Skip leading whitespace; accept an optional sign; read digits until a non-digit; clamp to the 32-bit signed range [-2147483648, 2147483647]. Return 0 if no digits are read.",
        "func_sig": "def my_atoi(s: str) -> int:",
        "tests": [
            "assert my_atoi('42') == 42",
            "assert my_atoi('   -42') == -42",
            "assert my_atoi('4193 with words') == 4193",
            "assert my_atoi('words and 987') == 0",
            "assert my_atoi('-91283472332') == -2147483648",
            "assert my_atoi('+1') == 1",
            "assert my_atoi('') == 0",
            "assert my_atoi('3.14') == 3",
        ],
    },
    {
        "name": "longest_substring_no_repeat",
        "prompt": "Write a function that returns the length of the longest substring without repeating characters.",
        "func_sig": "def length_of_longest_substring(s: str) -> int:",
        "tests": [
            "assert length_of_longest_substring('abcabcbb') == 3",
            "assert length_of_longest_substring('bbbbb') == 1",
            "assert length_of_longest_substring('pwwkew') == 3",
            "assert length_of_longest_substring('') == 0",
            "assert length_of_longest_substring('au') == 2",
            "assert length_of_longest_substring('dvdf') == 3",
        ],
    },
    {
        "name": "max_area_container",
        "prompt": "Write a function that finds the maximum amount of water a container can hold given an array of heights, where the container is formed by two vertical lines and the x-axis. Return the max area.",
        "func_sig": "def max_area(height: list[int]) -> int:",
        "tests": [
            "assert max_area([1,8,6,2,5,4,8,3,7]) == 49",
            "assert max_area([1,1]) == 1",
            "assert max_area([4,3,2,1,4]) == 16",
            "assert max_area([1,2,1]) == 2",
            "assert max_area([2,3,4,5,18,17,6]) == 17",
        ],
    },
    {
        "name": "interval_merge",
        "prompt": "Write a function that merges all overlapping intervals in a list of [start, end] pairs and returns the merged intervals, sorted by start. Adjacent intervals (end == next start) merge.",
        "func_sig": "def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:",
        "tests": [
            "assert merge_intervals([[1,3],[2,6],[8,10],[15,18]]) == [[1,6],[8,10],[15,18]]",
            "assert merge_intervals([[1,4],[4,5]]) == [[1,5]]",
            "assert merge_intervals([[1,4],[2,3]]) == [[1,4]]",
            "assert merge_intervals([]) == []",
            "assert merge_intervals([[1,4]]) == [[1,4]]",
            "assert merge_intervals([[1,4],[0,2],[3,5]]) == [[0,5]]",
        ],
    },
    {
        "name": "rotate_image",
        "prompt": "Write a function that rotates an n x n matrix 90 degrees clockwise IN PLACE (modify the input matrix, return None).",
        "func_sig": "def rotate(matrix: list[list[int]]) -> None:",
        "tests": [
            "m = [[1,2,3],[4,5,6],[7,8,9]]; rotate(m); assert m == [[7,4,1],[8,5,2],[9,6,3]]",
            "m = [[1]]; rotate(m); assert m == [[1]]",
            "m = [[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]]; rotate(m); assert m == [[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]]",
            "m = [[1,2],[3,4]]; rotate(m); assert m == [[3,1],[4,2]]",
        ],
    },
    {
        "name": "valid_bst",
        "prompt": "Write a function that returns True if a binary tree is a valid binary search tree: for every node, all values in its left subtree are strictly less than the node's value and all values in its right subtree are strictly greater.",
        "func_sig": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None): ...\n\ndef is_valid_bst(root: TreeNode | None) -> bool:",
        "tests": [
            "n = TreeNode(2, TreeNode(1), TreeNode(3)); assert is_valid_bst(n) == True",
            "n = TreeNode(5, TreeNode(1), TreeNode(4, TreeNode(3), TreeNode(6))); assert is_valid_bst(n) == False",
            "n = TreeNode(2, TreeNode(2), TreeNode(2)); assert is_valid_bst(n) == False",
            "assert is_valid_bst(None) == True",
            "n = TreeNode(5, TreeNode(4), TreeNode(6, TreeNode(3), TreeNode(7))); assert is_valid_bst(n) == False",
        ],
    },
    {
        "name": "lru_cache",
        "prompt": "Write an LRU cache class. get(key) returns the value (or -1 if absent); put(key, value) inserts or updates and evicts the least recently used key when capacity is exceeded. Both must run in O(1) average time.",
        "func_sig": "class LRUCache:\n    def __init__(self, capacity: int): ...\n    def get(self, key: int) -> int: ...\n    def put(self, key: int, value: int) -> None: ...",
        "tests": [
            "c = LRUCache(2); c.put(1,1); c.put(2,2); assert c.get(1)==1; c.put(3,3); assert c.get(2)==-1; c.put(4,4); assert c.get(1)==-1; assert c.get(3)==3; assert c.get(4)==4",
            "c = LRUCache(1); c.put(2,1); assert c.get(2)==1; c.put(3,2); assert c.get(2)==-1; assert c.get(3)==2",
            "c = LRUCache(2); assert c.get(2)==-1; c.put(2,6); assert c.get(1)==-1; c.put(1,5); c.put(1,2); assert c.get(1)==2; assert c.get(2)==6",
        ],
    },
    {
        "name": "trie_impl",
        "prompt": "Write a Trie class with insert(word), search(word) (exact match only), and starts_with(prefix).",
        "func_sig": "class Trie:\n    def __init__(self): ...\n    def insert(self, word: str) -> None: ...\n    def search(self, word: str) -> bool: ...\n    def starts_with(self, prefix: str) -> bool: ...",
        "tests": [
            "t = Trie(); t.insert('apple'); assert t.search('apple')==True; assert t.search('app')==False; assert t.starts_with('app')==True; t.insert('app'); assert t.search('app')==True",
            "t = Trie(); t.insert('a'); assert t.starts_with('a')==True; assert t.starts_with('ab')==False; t.insert('ab'); assert t.search('ab')==True",
            "t = Trie(); t.insert('hello'); t.insert('hell'); assert t.search('hell')==True; assert t.search('hello')==True; assert t.starts_with('he')==True",
        ],
    },
    {
        "name": "decode_string",
        "prompt": "Write a function that decodes an encoded string of the form k[encoded_string], where k is a positive integer (possibly multi-digit) and the content repeats k times. Nesting is allowed.",
        "func_sig": "def decode_string(s: str) -> str:",
        "tests": [
            "assert decode_string('3[a]2[bc]') == 'aaabcbc'",
            "assert decode_string('3[a2[c]]') == 'accaccacc'",
            "assert decode_string('2[abc]3[cd]ef') == 'abcabccdcdcdef'",
            "assert decode_string('abc3[cd]xyz') == 'abccdcdcdxyz'",
            "assert decode_string('10[a]') == 'aaaaaaaaaa'",
            "assert decode_string('') == ''",
        ],
    },
    {
        "name": "course_schedule",
        "prompt": "Write a function that returns True if all courses can be finished given the number of courses and a list of prerequisite pairs [course, prerequisite], where a cycle means they cannot.",
        "func_sig": "def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:",
        "tests": [
            "assert can_finish(2, [[1,0]]) == True",
            "assert can_finish(2, [[1,0],[0,1]]) == False",
            "assert can_finish(4, [[1,0],[2,0],[3,1],[3,2]]) == True",
            "assert can_finish(3, [[0,1],[1,2],[2,0]]) == False",
            "assert can_finish(1, []) == True",
            "assert can_finish(3, [[1,0],[0,1],[1,2]]) == False",
        ],
    },
    {
        "name": "min_window_substring",
        "prompt": "Write a function that returns the minimum window substring of s that contains all characters of t (including duplicates). Return '' if no such window exists.",
        "func_sig": "def min_window(s: str, t: str) -> str:",
        "tests": [
            "assert min_window('ADOBECODEBANC', 'ABC') == 'BANC'",
            "assert min_window('a', 'a') == 'a'",
            "assert min_window('a', 'aa') == ''",
            "assert min_window('ab', 'a') == 'a'",
            "assert min_window('cabwefgewcwaefgcf', 'cae') == 'cwae'",
        ],
    },
    {
        "name": "find_duplicate_number",
        "prompt": "Write a function that returns the duplicate number in an array of n+1 integers where each integer is in [1, n] and exactly one number appears more than once.",
        "func_sig": "def find_duplicate(nums: list[int]) -> int:",
        "tests": [
            "assert find_duplicate([1,3,4,2,2]) == 2",
            "assert find_duplicate([3,1,3,4,2]) == 3",
            "assert find_duplicate([1,1]) == 1",
            "assert find_duplicate([1,1,2]) == 1",
            "assert find_duplicate([2,2,2,2,2]) == 2",
        ],
    },
]
