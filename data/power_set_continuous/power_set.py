def power_set(nums):
    """
    Returns the power set of a given list of distinct integers.
    The power set is the set of all subsets of the input.
    
    Args:
        nums: A list of distinct integers
        
    Returns:
        A list of all subsets (each subset is a list)
    """
    result = []
    n = len(nums)
    
    # There are 2^n subsets for a set of n elements
    for i in range(2 ** n):
        subset = []
        for j in range(n):
            # Check if the j-th bit is set in i
            if i & (1 << j):
                subset.append(nums[j])
        result.append(subset)
    
    return result
