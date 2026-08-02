def climbing_stairs(n: int) -> int:
    """Return the number of distinct ways to climb n steps taking 1 or 2 steps.

    Behavior:
    - If n < 0: return 0
    - If n == 0: return 1
    - For n >= 1: compute ways using recurrence ways(n)=ways(n-1)+ways(n-2).

    Raises TypeError if n is not an int.
    """
    if not isinstance(n, int):
        raise TypeError("n must be an int")
    if n < 0:
        return 0
    if n == 0:
        return 1
    if n == 1:
        return 1
    a, b = 1, 1  # ways(0)=1, ways(1)=1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
