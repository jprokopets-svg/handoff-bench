from typing import List


def max_area(height: List[int]) -> int:
    """Return the maximum area of water container formed by two lines in height."""
    if not height:
        return 0
    left = 0
    right = len(height) - 1
    max_area_val = 0
    while left < right:
        h = min(height[left], height[right])
        width = right - left
        area = h * width
        if area > max_area_val:
            max_area_val = area
        # Move the pointer at the shorter line inward
        if height[left] < height[right]:
            left += 1
        elif height[left] > height[right]:
            right -= 1
        else:
            # equal heights: move both
            left += 1
            right -= 1
    return max_area_val
