from typing import List


def max_area(height: List[int]) -> int:
    """Return the max area of water container formed by two vertical lines.

    Uses two-pointer technique: start with left at 0 and right at len(height)-1,
    compute area = min(h[left], h[right]) * (right-left), update max, then
    move the pointer at the smaller height inward. Time O(n), space O(1).
    """
    if not height or len(height) < 2:
        return 0

    left = 0
    right = len(height) - 1
    max_area_val = 0

    while left < right:
        h_left = height[left]
        h_right = height[right]
        current_area = min(h_left, h_right) * (right - left)
        if current_area > max_area_val:
            max_area_val = current_area

        # Move the pointer at the smaller height inward; if equal, move right
        if h_left < h_right:
            left += 1
        else:
            right -= 1

    return max_area_val
