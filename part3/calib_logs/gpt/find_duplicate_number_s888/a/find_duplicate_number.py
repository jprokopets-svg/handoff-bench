def find_duplicate(nums):
    """
    Find the duplicate number in an array of n+1 integers where each integer is in [1, n]
    and there is exactly one number that appears more than once (could be repeated multiple times).

    Uses Floyd's Tortoise and Hare (cycle detection) to find the duplicate in O(n) time
    and O(1) extra space without modifying the input.
    """
    if not nums:
        raise ValueError("nums must be non-empty")

    # Phase 1: Find intersection point of two runners.
    tortoise = nums[0]
    hare = nums[0]
    while True:
        tortoise = nums[tortoise]
        hare = nums[nums[hare]]
        if tortoise == hare:
            break

    # Phase 2: Find the entrance to the cycle.
    ptr1 = nums[0]
    ptr2 = tortoise
    while ptr1 != ptr2:
        ptr1 = nums[ptr1]
        ptr2 = nums[ptr2]

    return ptr1
