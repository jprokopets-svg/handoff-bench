def find_duplicate(nums):
    """Find the duplicate number in an array of n+1 integers where each integer is in [1, n].

    Uses Floyd's Tortoise and Hare (cycle detection) algorithm to find the duplicate
    in O(n) time and O(1) extra space without modifying the input.
    """
    if not nums:
        raise ValueError("nums must be non-empty")

    # Initialize tortoise and hare
    tortoise = nums[0]
    hare = nums[0]

    # First phase: find intersection point inside the cycle
    while True:
        tortoise = nums[tortoise]
        hare = nums[nums[hare]]
        if tortoise == hare:
            break

    # Second phase: find the entrance to the cycle (the duplicate number)
    ptr1 = nums[0]
    ptr2 = tortoise
    while ptr1 != ptr2:
        ptr1 = nums[ptr1]
        ptr2 = nums[ptr2]

    return ptr1
