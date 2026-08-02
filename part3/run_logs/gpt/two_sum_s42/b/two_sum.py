from typing import List


def two_sum(nums: List[int], target: int) -> List[int]:
    """Return indices [i, j] (i < j) of the two numbers in nums that add up to target.

    Assumes exactly one solution exists and the same element cannot be used twice.
    If no solution is found, raises ValueError.
    """
    seen = {}  # value -> index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            j = i
            i0 = seen[complement]
            # ensure smaller index first
            if i0 < j:
                return [i0, j]
            else:
                return [j, i0]
        # store the first occurrence index for a value
        if num not in seen:
            seen[num] = i
    raise ValueError("No two sum solution")
