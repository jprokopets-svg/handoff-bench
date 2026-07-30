def three_sum(nums: list[int]) -> list[list[int]]:
    """
    Find all unique triplets in an array that sum to zero.
    
    Args:
        nums: List of integers
        
    Returns:
        List of unique triplets that sum to zero, sorted
    """
    nums.sort()
    result = []
    n = len(nums)
    
    for i in range(n - 2):
        # If the current number is positive, no triplet can sum to zero
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
                
                # Skip duplicates for the left pointer
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                # Skip duplicates for the right pointer
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
            elif current_sum < target:
                left += 1
            else:
                right -= 1
    
    return result
