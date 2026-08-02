def max_area(heights):
    """
    Find the maximum area of water that can be contained.
    
    The container is formed by two vertical lines at indices i and j,
    where the area is: (j - i) * min(heights[i], heights[j])
    
    Args:
        heights: List of integers representing heights
        
    Returns:
        Integer representing the maximum area
    """
    if not heights or len(heights) < 2:
        return 0
    
    max_area_val = 0
    left = 0
    right = len(heights) - 1
    
    # Two-pointer approach: start from both ends and move inward
    while left < right:
        # Calculate current area
        width = right - left
        current_height = min(heights[left], heights[right])
        current_area = width * current_height
        
        # Update max area
        max_area_val = max(max_area_val, current_area)
        
        # Move the pointer pointing to the shorter line inward
        # This is because the area is limited by the shorter line,
        # so we need to try to find a taller line
        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1
    
    return max_area_val
