def three_sum(nums):
    """
    Find all unique triplets in the array that sum to zero.
    
    Args:
        nums: List of integers
        
    Returns:
        List of lists, where each inner list is a triplet that sums to zero.
        Each triplet should be sorted, and the result should contain unique triplets.
    """
    nums.sort()
    result = []
    n = len(nums)
    
    for i in range(n - 2):
        # If current number is positive, no triplet can sum to zero
        if nums[i] > 0:
            break
        
        # Skip duplicate values for the first element
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        # Use two pointers to find pairs that sum to -nums[i]
        left = i + 1
        right = n - 1
        target = -nums[i]
        
        while left < right:
            current_sum = nums[left] + nums[right]
            
            if current_sum == target:
                result.append([nums[i], nums[left], nums[right]])
                
                # Skip duplicate values for the second element
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                # Skip duplicate values for the third element
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
            elif current_sum < target:
                left += 1
            else:
                right -= 1
    
    return result
