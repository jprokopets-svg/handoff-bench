def two_sum(nums, target):
    """Return indices of the two numbers that add up to target.
    Assumes exactly one solution and you may not use the same element twice.
    Returns a list [i, j] with i < j (the earlier index first).
    """
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    # If no solution found (shouldn't happen given problem constraints), raise error
    raise ValueError("No two sum solution")
