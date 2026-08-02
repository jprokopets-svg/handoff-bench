def max_area(height: list[int]) -> int:
    """
    Find the maximum area of water that can be contained between two vertical lines.
    
    Uses a two-pointer approach starting from both ends of the array and moving
    inward by advancing the pointer at the shorter height.
    
    Args:
        height: List of integers representing heights of vertical lines
        
    Returns:
        Maximum area that can be contained
        
    Time Complexity: O(n) - single pass through the array
    Space Complexity: O(1) - constant space
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
        
        # Move the pointer at the shorter height inward
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return max_area_val
