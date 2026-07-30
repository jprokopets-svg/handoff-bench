def longest_palindrome(s: str) -> str:
    """
    Returns the longest palindromic substring in a given string.
    
    Args:
        s: Input string
        
    Returns:
        The longest palindromic substring. If multiple palindromes of the same
        length exist, returns one of them.
    """
    if not s:
        return ""
    
    def expand_around_center(left: int, right: int) -> tuple:
        """
        Expands around a center point and returns the start and end indices
        of the palindrome found.
        """
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        # Return the valid palindrome boundaries
        return left + 1, right - 1
    
    start = 0
    end = 0
    
    for i in range(len(s)):
        # Check for odd-length palindromes (single character center)
        left1, right1 = expand_around_center(i, i)
        
        # Check for even-length palindromes (two character center)
        left2, right2 = expand_around_center(i, i + 1)
        
        # Update if we found a longer palindrome
        if right1 - left1 > end - start:
            start, end = left1, right1
        
        if right2 - left2 > end - start:
            start, end = left2, right2
    
    return s[start:end + 1]
