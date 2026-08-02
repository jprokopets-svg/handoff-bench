def count_bits(n: int) -> int:
    """Return the number of 1 bits in the binary representation of n.

    n should be a non-negative integer.
    """
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")
    return bin(n).count('1')
