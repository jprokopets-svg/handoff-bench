def find_duplicate(nums: list[int]) -> int:
    """Find the duplicate number in an array of n+1 integers where each integer is in [1, n].

    Uses Floyd's Tortoise and Hare (cycle detection) algorithm which runs in O(n) time
    and O(1) extra space.

    Raises ValueError for empty or malformed input.
    """
    if not isinstance(nums, list):
        raise ValueError("Input must be a list of integers")
    if len(nums) < 2:
        raise ValueError("Input list must contain at least two elements")

    # Floyd's cycle-finding algorithm
    try:
        tortoise = nums[0]
        hare = nums[0]
        # First phase: find intersection point inside the cycle
        while True:
            tortoise = nums[tortoise]
            hare = nums[nums[hare]]
            if tortoise == hare:
                break
        # Second phase: find the entrance to the cycle (duplicate)
        ptr1 = nums[0]
        ptr2 = tortoise
        while ptr1 != ptr2:
            ptr1 = nums[ptr1]
            ptr2 = nums[ptr2]
        return ptr1
    except (IndexError, TypeError) as e:
        # IndexError can occur if values are out of expected range, TypeError if non-integers
        raise ValueError("Invalid input: elements must be integers in the range [1, n]") from e
