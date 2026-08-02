def count_bits(n: int) -> int:
    """
    Returns the number of 1 bits in the binary representation of a non-negative integer.
    
    Args:
        n: A non-negative integer
        
    Returns:
        The count of 1 bits in the binary representation of n
        
    Examples:
        count_bits(0) == 0      # binary: 0
        count_bits(5) == 2      # binary: 101
        count_bits(255) == 8    # binary: 11111111
        count_bits(1023) == 10  # binary: 1111111111
    """
    return bin(n).count('1')
