from typing import List


def max_area(height: List[int]) -> int:
    """Return the maximum area of water that can be contained.

    Uses two-pointer technique: move pointer at shorter line inward.
    """
    if not height or len(height) < 2:
        return 0

    left = 0
    right = len(height) - 1
    max_area_val = 0

    while left < right:
        h_left = height[left]
        h_right = height[right]
        width = right - left
        current_area = min(h_left, h_right) * width
        if current_area > max_area_val:
            max_area_val = current_area

        # Move the pointer at the smaller height inward
        if h_left < h_right:
            left += 1
        elif h_left > h_right:
            right -= 1
        else:
            # heights equal - move both to try find taller lines
            left += 1
            right -= 1

    return max_area_val
