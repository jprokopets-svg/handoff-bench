def find_duplicate(nums: list[int]) -> int:
    # Input validation
    if not nums or len(nums) < 2:
        raise ValueError("Input list must have at least 2 elements")
    
    # Floyd's cycle detection algorithm
    # Phase 1: Find intersection point
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
    
    return hare