def fibonacci(n: int) -> int:
    """
    Returns the nth Fibonacci number where fib(0) = 0 and fib(1) = 1.
    
    For n >= 2, fib(n) = fib(n-1) + fib(n-2)
    
    Args:
        n: The index of the Fibonacci number to compute
        
    Returns:
        The nth Fibonacci number
    """
    if n == 0:
        return 0
    if n == 1:
        return 1
    
    # Iterative approach: O(n) time, O(1) space
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    
    return b
