def longest_palindrome(s):
    """
    Returns the longest palindromic substring in a given string.
    
    Args:
        s: A string
        
    Returns:
        The longest palindromic substring. If multiple palindromes of the same
        length exist, any one of them can be returned.
    """
    if not s:
        return ""
    
    def expand_around_center(left, right):
        """Expand around center and return the palindrome found."""
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        # Return the valid palindrome (left and right are one step too far)
        return s[left + 1:right]
    
    longest = ""
    
    for i in range(len(s)):
        # Check for odd-length palindromes (single character center)
        palindrome1 = expand_around_center(i, i)
        if len(palindrome1) > len(longest):
            longest = palindrome1
        
        # Check for even-length palindromes (two character center)
        palindrome2 = expand_around_center(i, i + 1)
        if len(palindrome2) > len(longest):
            longest = palindrome2
    
    return longest
