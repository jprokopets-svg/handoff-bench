def power_set(nums):
    """
    Returns the power set of a given set of distinct integers.
    
    The power set is the set of all subsets of the input set.
    For a set with n elements, the power set has 2^n elements.
    
    Args:
        nums: A list of distinct integers
        
    Returns:
        A list of lists, where each inner list is a subset of nums
    """
    result = []
    n = len(nums)
    
    # Iterate through all possible subsets using bit manipulation
    # For n elements, there are 2^n subsets
    for i in range(2 ** n):
        subset = []
        for j in range(n):
            # Check if the j-th bit is set in i
            if i & (1 << j):
                subset.append(nums[j])
        result.append(subset)
    
    return result
