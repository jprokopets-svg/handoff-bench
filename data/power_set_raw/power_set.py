def power_set(nums):
    """
    Returns the power set of a given set of distinct integers.
    The power set is the set of all subsets of the input set.
    
    Args:
        nums: A list of distinct integers
        
    Returns:
        A list of lists, where each inner list is a subset of nums
    """
    result = []
    n = len(nums)
    
    # There are 2^n subsets in the power set
    for i in range(2 ** n):
        subset = []
        for j in range(n):
            # Check if the j-th bit is set in i
            if i & (1 << j):
                subset.append(nums[j])
        result.append(subset)
    
    return result
