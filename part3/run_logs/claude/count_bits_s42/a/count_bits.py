def count_bits(n):
    """
    Returns the number of 1 bits in the binary representation of a non-negative integer.
    
    Args:
        n: A non-negative integer
        
    Returns:
        The count of 1 bits in the binary representation of n
    """
    return bin(n).count('1')
