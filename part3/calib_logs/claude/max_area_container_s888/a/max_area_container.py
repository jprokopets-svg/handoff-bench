def max_area(heights):
    """
    Find the maximum area of water that can be contained between two vertical lines.
    
    Args:
        heights: List of integers representing the heights of vertical lines
        
    Returns:
        Integer representing the maximum area
    """
    if not heights or len(heights) < 2:
        return 0
    
    max_area_val = 0
    left = 0
    right = len(heights) - 1
    
    # Two-pointer approach
    while left < right:
        # Calculate current area
        width = right - left
        current_height = min(heights[left], heights[right])
        current_area = width * current_height
        
        # Update max area
        max_area_val = max(max_area_val, current_area)
        
        # Move the pointer pointing to the shorter line
        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1
    
    return max_area_val
