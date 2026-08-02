def find_duplicate(nums: list[int]) -> int:
    """
    Find the duplicate number in an array of n+1 integers where each integer is in [1, n].
    
    Uses Floyd's Cycle Detection algorithm (tortoise and hare):
    - Treats the array as a linked list where nums[i] points to index nums[i]
    - Since there's a duplicate, there must be a cycle
    - The entrance to the cycle is the duplicate number
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    
    Args:
        nums: List of n+1 integers where each is in range [1, n] with exactly one duplicate
        
    Returns:
        The duplicate number
        
    Example:
        >>> find_duplicate([1,3,4,2,2])
        2
        >>> find_duplicate([3,1,3,4,2])
        3
    """
    # Phase 1: Detect cycle using tortoise and hare
    # Tortoise moves 1 step, hare moves 2 steps
    tortoise = nums[0]
    hare = nums[0]
    
    # Move until they meet (cycle detection)
    while True:
        tortoise = nums[tortoise]
        hare = nums[nums[hare]]
        if tortoise == hare:
            break
    
    # Phase 2: Find cycle entrance (which is the duplicate number)
    # Move one pointer to start, move both 1 step at a time
    # They will meet at the cycle entrance
    tortoise = nums[0]
    while tortoise != hare:
        tortoise = nums[tortoise]
        hare = nums[hare]
    
    return tortoise
