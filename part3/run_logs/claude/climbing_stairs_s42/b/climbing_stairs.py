def climbing_stairs(n: int) -> int:
    """
    Calculate the number of distinct ways to climb an n-step staircase.
    
    You can take either 1 or 2 steps at a time.
    
    Args:
        n: The number of steps in the staircase
        
    Returns:
        The number of distinct ways to climb the staircase
        
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    # Base cases
    if n <= 0:
        return 0
    if n == 1:
        return 1
    if n == 2:
        return 2
    
    # Use dynamic programming with space optimization
    # prev2 represents ways to reach (i-2)th step
    # prev1 represents ways to reach (i-1)th step
    prev2 = 1  # ways to reach step 1
    prev1 = 2  # ways to reach step 2
    
    # Calculate for steps 3 to n
    for i in range(3, n + 1):
        current = prev1 + prev2
        prev2 = prev1
        prev1 = current
    
    return prev1
