def find_duplicate(nums):
    """
    Find the duplicate number in an array of n+1 integers where each integer
    is in the range [1, n] and exactly one number appears more than once.
    
    Uses Floyd's Tortoise and Hare algorithm (cycle detection).
    
    Args:
        nums: List of integers where each integer is in [1, n] and there are n+1 elements
        
    Returns:
        The duplicate integer
    """
    # Phase 1: Find the intersection point of the two runners
    tortoise = nums[0]
    hare = nums[0]
    
    while True:
        tortoise = nums[tortoise]
        hare = nums[nums[hare]]
        if tortoise == hare:
            break
    
    # Phase 2: Find the entrance to the cycle
    tortoise = nums[0]
    while tortoise != hare:
        tortoise = nums[tortoise]
        hare = nums[hare]
    
    return tortoise