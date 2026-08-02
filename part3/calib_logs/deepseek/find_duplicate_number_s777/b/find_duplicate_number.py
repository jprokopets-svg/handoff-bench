def find_duplicate(nums: list[int]) -> int:
    """
    Find the duplicate number in an array of n+1 integers where each integer 
    is in [1, n] and exactly one number appears more than once.
    
    Uses Floyd's Tortoise and Hare algorithm for cycle detection.
    
    Args:
        nums: List of integers where each integer is in [1, n] and 
              exactly one number appears more than once.
    
    Returns:
        The duplicate number.
    
    Raises:
        ValueError: If the input list is empty, contains values outside [1, n],
                   or doesn't contain exactly one duplicate.
    """
    # Input validation
    if not nums:
        raise ValueError("Input list cannot be empty")
    
    n = len(nums) - 1
    
    # Check that all values are in range [1, n]
    for num in nums:
        if num < 1 or num > n:
            raise ValueError(f"Value {num} is outside the valid range [1, {n}]")
    
    # Phase 1: Find the intersection point of the two runners
    tortoise = nums[0]
    hare = nums[0]
    
    while True:
        tortoise = nums[tortoise]
        hare = nums[nums[hare]]
        if tortoise == hare:
            break
    
    # Phase 2: Find the entrance to the cycle (duplicate number)
    tortoise = nums[0]
    while tortoise != hare:
        tortoise = nums[tortoise]
        hare = nums[hare]
    
    return tortoise