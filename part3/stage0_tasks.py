#!/usr/bin/env python3
"""part3/stage0_tasks.py — Stage 0 non-study tasks.

Five simple tasks. Disjoint from the V2 task set (regex_parser, n_queens,
median_stream, word_break, median_two_sorted, serialize_tree, max_path_sum,
merge_k_lists) and from calib-bench task sets. Per STAGE0_PREREG.md (f),
these tasks are excluded from any future tier and never reused as study tasks.
"""

STAGE0_TASKS = [
    {
        "name": "two_sum",
        "prompt": "Write a function that returns the indices of the two numbers in a list that add up to a target. Assume exactly one solution exists and you may not use the same element twice.",
        "func_sig": "def two_sum(nums: list[int], target: int) -> list[int]:",
        "tests": [
            "assert two_sum([2, 7, 11, 15], 9) == [0, 1]",
            "assert two_sum([3, 2, 4], 6) == [1, 2]",
            "assert two_sum([3, 3], 6) == [0, 1]",
            "assert two_sum([-1, 0, 1], 0) == [0, 2]",
        ],
    },
    {
        "name": "valid_palindrome",
        "prompt": "Write a function that returns True if a string is a palindrome, ignoring non-alphanumeric characters and case. For example, 'A man, a plan, a canal: Panama' is a palindrome.",
        "func_sig": "def valid_palindrome(s: str) -> bool:",
        "tests": [
            "assert valid_palindrome('A man, a plan, a canal: Panama') == True",
            "assert valid_palindrome('race a car') == False",
            "assert valid_palindrome(' ') == True",
            "assert valid_palindrome('ab_a') == True",
        ],
    },
    {
        "name": "fibonacci",
        "prompt": "Write a function that returns the nth Fibonacci number, where fib(0) = 0 and fib(1) = 1.",
        "func_sig": "def fibonacci(n: int) -> int:",
        "tests": [
            "assert fibonacci(0) == 0",
            "assert fibonacci(1) == 1",
            "assert fibonacci(10) == 55",
            "assert fibonacci(25) == 75025",
        ],
    },
    {
        "name": "count_bits",
        "prompt": "Write a function that returns the number of 1 bits in the binary representation of a non-negative integer (the population count).",
        "func_sig": "def count_bits(n: int) -> int:",
        "tests": [
            "assert count_bits(0) == 0",
            "assert count_bits(5) == 2",
            "assert count_bits(255) == 8",
            "assert count_bits(1023) == 10",
        ],
    },
    {
        "name": "climbing_stairs",
        "prompt": "Write a function that returns the number of distinct ways to climb a staircase of n steps, taking either 1 or 2 steps at a time.",
        "func_sig": "def climbing_stairs(n: int) -> int:",
        "tests": [
            "assert climbing_stairs(1) == 1",
            "assert climbing_stairs(2) == 2",
            "assert climbing_stairs(3) == 3",
            "assert climbing_stairs(5) == 8",
        ],
    },
]
