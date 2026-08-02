def count_bits(n: int) -> int:
    """Return the number of 1 bits in the binary representation of a non-negative integer n.

    Args:
        n: A non-negative integer.

    Returns:
        The population count (number of 1 bits) of n.

    Raises:
        TypeError: If n is not an int.
        ValueError: If n is negative.
    """
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")
    # Use Python's binary representation and count '1' characters.
    return bin(n).count('1')
