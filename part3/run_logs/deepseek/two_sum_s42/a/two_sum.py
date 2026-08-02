def two_sum(nums, target):
    """
    Return indices of the two numbers such that they add up to target.
    
    Args:
        nums: List of integers
        target: Integer target sum
        
    Returns:
        List of two indices
    """
    # Dictionary to store number -> index mapping
    num_map = {}
    
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    
    # According to the problem, exactly one solution exists,
    # so we should never reach this point
    return []