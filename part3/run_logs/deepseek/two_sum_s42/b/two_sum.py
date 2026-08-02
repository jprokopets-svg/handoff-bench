def two_sum(nums: list[int], target: int) -> list[int]:
    """
    Return indices of the two numbers in nums that add up to target.
    
    Args:
        nums: List of integers
        target: Target sum
        
    Returns:
        List of two indices [i, j] such that nums[i] + nums[j] == target
    """
    # Create a dictionary to store number -> index mapping
    num_to_index = {}
    
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_to_index:
            return [num_to_index[complement], i]
        num_to_index[num] = i
    
    # According to the problem statement, exactly one solution exists,
    # so we should never reach this point
    return []