def trap(height):
    """
    Calculate how much water can be trapped after raining.
    
    Args:
        height: List of non-negative integers representing elevation heights
        
    Returns:
        Integer representing the total amount of water trapped
    """
    if not height or len(height) < 3:
        return 0
    
    n = len(height)
    
    # Calculate the maximum height to the left of each position
    left_max = [0] * n
    left_max[0] = height[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i-1], height[i])
    
    # Calculate the maximum height to the right of each position
    right_max = [0] * n
    right_max[n-1] = height[n-1]
    for i in range(n-2, -1, -1):
        right_max[i] = max(right_max[i+1], height[i])
    
    # Calculate trapped water
    water = 0
    for i in range(n):
        # Water level at position i is determined by the minimum of
        # the maximum heights on both sides
        water_level = min(left_max[i], right_max[i])
        # Water trapped at position i is the difference between water level and ground height
        water += max(0, water_level - height[i])
    
    return water
