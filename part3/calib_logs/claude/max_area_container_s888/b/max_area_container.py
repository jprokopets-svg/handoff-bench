def max_area(height: list[int]) -> int:
    """
    Find the maximum area of water that can be contained between two vertical lines.
    
    Uses a two-pointer approach starting from both ends and moving inward,
    always moving the pointer pointing to the shorter line to explore potentially
    larger areas.
    
    Args:
        height: List of integers representing the height of vertical lines
        
    Returns:
        The maximum area that can be contained
        
    Examples:
        >>> max_area([1,8,6,2,5,4,8,3,7])
        49
        >>> max_area([1,1])
        1
        >>> max_area([1,2,1])
        2
    """
    if not height or len(height) < 2:
        return 0
    
    max_area_val = 0
    left = 0
    right = len(height) - 1
    
    while left < right:
        # Calculate current area
        width = right - left
        current_height = min(height[left], height[right])
        current_area = width * current_height
        
        # Update max area
        max_area_val = max(max_area_val, current_area)
        
        # Move the pointer pointing to the shorter line
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return max_area_val
