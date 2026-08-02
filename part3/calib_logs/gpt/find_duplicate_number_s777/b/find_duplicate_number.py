from typing import List


def find_duplicate(nums: List[int]) -> int:
    """Find the duplicate number in an array of n+1 integers where each integer is in [1, n].

    Uses Floyd's Tortoise and Hare (cycle detection) algorithm to find the duplicate
    in O(n) time and O(1) extra space without modifying the input list.

    Validates input: raises ValueError if nums is empty or if any element is not an int
    or not in the valid range [1, len(nums)-1].
    """
    if not nums:
        raise ValueError("Input list must not be empty")

    m = len(nums)
    n = m - 1

    # Validate elements
    for i, x in enumerate(nums):
        if not isinstance(x, int):
            raise ValueError(f"All elements must be integers; element at index {i} is {type(x)}")
        if x < 1 or x > n:
            raise ValueError(f"All elements must be in range [1, {n}]; element at index {i} is {x}")

    # Floyd's Tortoise and Hare
    tortoise = nums[0]
    hare = nums[0]

    while True:
        tortoise = nums[tortoise]
        hare = nums[nums[hare]]
        if tortoise == hare:
            break

    # Find entrance to the cycle
    ptr1 = nums[0]
    ptr2 = tortoise
    while ptr1 != ptr2:
        ptr1 = nums[ptr1]
        ptr2 = nums[ptr2]

    return ptr1
