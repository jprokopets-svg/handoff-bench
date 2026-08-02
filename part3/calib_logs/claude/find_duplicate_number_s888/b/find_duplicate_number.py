def find_duplicate(nums: list[int]) -> int:
    """
    Find the duplicate number in an array of n+1 integers where each integer is in [1, n].
    
    Uses Floyd's Cycle Detection algorithm (tortoise and hare):
    - Treats the array as a linked list where nums[i] points to index nums[i]
    - Phase 1: Detect cycle by moving slow pointer 1 step and fast pointer 2 steps
    - Phase 2: Find cycle entrance (the duplicate) by moving both pointers 1 step at a time
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    
    Args:
        nums: List of n+1 integers where each integer is in range [1, n]
        
    Returns:
        The duplicate number
    """
    # Phase 1: Detect cycle
    slow = nums[0]
    fast = nums[0]
    
    # Move slow pointer 1 step and fast pointer 2 steps until they meet
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    
    # Phase 2: Find cycle entrance (the duplicate number)
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    
    return slow
