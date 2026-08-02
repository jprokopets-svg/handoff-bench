def max_area(height: list[int]) -> int:
    left = 0
    right = len(height) - 1
    max_area_val = 0

    while left < right:
        current_area = min(height[left], height[right]) * (right - left)
        max_area_val = max(max_area_val, current_area)

        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return max_area_val