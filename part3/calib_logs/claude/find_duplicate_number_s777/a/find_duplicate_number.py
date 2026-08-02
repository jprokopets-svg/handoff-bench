def find_duplicate(nums):
    """
    Find the duplicate number in an array of n+1 integers where each integer is in [1, n]
    and exactly one number appears more than once.
    
    Args:
        nums: List of integers
        
    Returns:
        The duplicate number
    """
    # Using Floyd's cycle detection algorithm (tortoise and hare)
    # This works because we can treat the array as a linked list where
    # nums[i] points to index nums[i]
    
    # Phase 1: Find intersection point in the cycle
    slow = nums[0]
    fast = nums[0]
    
    # Move slow by 1 step and fast by 2 steps
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    
    # Phase 2: Find the entrance to the cycle (the duplicate number)
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    
    return slow
