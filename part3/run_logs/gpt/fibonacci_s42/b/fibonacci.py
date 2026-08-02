def fibonacci(n: int) -> int:
    """Return the nth Fibonacci number with fib(0)=0 and fib(1)=1.

    Args:
        n: A non-negative integer index.

    Returns:
        The nth Fibonacci number as an int.

    Raises:
        TypeError: if n is not an int or is a bool.
        ValueError: if n is negative.
    """
    # Reject booleans explicitly (they are instances of int in Python)
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be an int")
    if n < 0:
        raise ValueError("n must be non-negative")

    # Fast doubling method: returns (F(n), F(n+1))
    def _fib_pair(k: int) -> tuple[int, int]:
        if k == 0:
            return (0, 1)
        a, b = _fib_pair(k >> 1)
        c = a * ((b << 1) - a)  # F(2m) = F(m) * (2*F(m+1) − F(m))
        d = a * a + b * b      # F(2m+1) = F(m)^2 + F(m+1)^2
        if k & 1:
            return (d, c + d)
        else:
            return (c, d)

    return _fib_pair(n)[0]
