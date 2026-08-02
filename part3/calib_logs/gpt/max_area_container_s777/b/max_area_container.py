from typing import List


def max_area(height: List[int]) -> int:
    """Return the maximum area of water that can be contained.

    Uses the two-pointer approach: start with pointers at both ends and move
    the pointer at the smaller height inward to try to find a taller line.

    Time complexity: O(n), Space complexity: O(1).
    """
    n = len(height)
    if n < 2:
        return 0

    left, right = 0, n - 1
    max_a = 0

    while left < right:
        h_left = height[left]
        h_right = height[right]
        width = right - left
        # area is bounded by the shorter line
        area = min(h_left, h_right) * width
        if area > max_a:
            max_a = area

        # Move the pointer pointing to the shorter line inward
        if h_left < h_right:
            left += 1
        elif h_left > h_right:
            right -= 1
        else:
            # heights equal: moving either pointer is fine; move both to
            # potentially converge faster
            left += 1
            right -= 1

    return max_a
