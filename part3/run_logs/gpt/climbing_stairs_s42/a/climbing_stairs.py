def climbing_stairs(n: int) -> int:
    """Return the number of distinct ways to climb n steps taking 1 or 2 steps at a time.

    For n < 0: return 0. For n == 0: there is one way (do nothing).
    Uses an iterative Fibonacci-like approach: ways(n) = ways(n-1) + ways(n-2),
    with ways(0)=1, ways(1)=1 (so ways(2)=2).
    """
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n < 0:
        return 0
    if n == 0:
        return 1
    if n == 1:
        return 1
    # iterative computation
    a, b = 1, 1  # a = ways(0), b = ways(1)
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
