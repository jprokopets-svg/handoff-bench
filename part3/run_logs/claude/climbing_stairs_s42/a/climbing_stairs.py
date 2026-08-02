def climbing_stairs(n):
    """
    Returns the number of distinct ways to climb a staircase of n steps,
    taking either 1 or 2 steps at a time.
    
    This follows the Fibonacci sequence pattern:
    - To reach step n, you can either come from step (n-1) by taking 1 step,
      or from step (n-2) by taking 2 steps.
    - So ways(n) = ways(n-1) + ways(n-2)
    
    Args:
        n: Number of steps in the staircase
        
    Returns:
        Number of distinct ways to climb n steps
    """
    if n <= 0:
        return 0
    if n == 1:
        return 1
    if n == 2:
        return 2
    
    # Use dynamic programming to avoid redundant calculations
    prev2 = 1  # ways to climb 1 step
    prev1 = 2  # ways to climb 2 steps
    
    for i in range(3, n + 1):
        current = prev1 + prev2
        prev2 = prev1
        prev1 = current
    
    return prev1
