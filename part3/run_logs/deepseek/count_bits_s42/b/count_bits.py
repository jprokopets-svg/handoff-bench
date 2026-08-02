def count_bits(n: int) -> int:
    """Return the number of 1 bits in the binary representation of n.
    
    Args:
        n: A non-negative integer.
        
    Returns:
        The number of 1 bits in n's binary representation.
    """
    count = 0
    while n > 0:
        count += n & 1  # Add 1 if the least significant bit is 1
        n >>= 1  # Right shift by 1 bit
    return count