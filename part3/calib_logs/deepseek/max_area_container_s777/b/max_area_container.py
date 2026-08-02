def max_area(height: list[int]) -> int:
    """
    Calculate the maximum area of water that can be contained between two vertical lines.
    
    The area is calculated as: min(height[left], height[right]) * (right - left)
    
    Args:
        height: List of integers representing the heights of vertical lines
        
    Returns:
        Maximum area of water that can be contained
    """
    if not height or len(height) < 2:
        return 0
    
    left = 0
    right = len(height) - 1
    max_area = 0
    
    while left < right:
        # Calculate current area
        current_area = min(height[left], height[right]) * (right - left)
        max_area = max(max_area, current_area)
        
        # Move the pointer with smaller height inward
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return max_area