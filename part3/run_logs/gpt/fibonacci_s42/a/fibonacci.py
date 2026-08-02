def fibonacci(n):
    """Return the nth Fibonacci number with fib(0)=0, fib(1)=1.

    Parameters
    - n: non-negative integer
    """
    # Validate input
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")

    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
