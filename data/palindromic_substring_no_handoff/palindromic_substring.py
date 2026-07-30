def longest_palindrome(s: str) -> str:
    """
    Returns the longest palindromic substring in a given string.
    
    Uses the expand-around-center approach:
    - For each possible center (both single character and between characters),
      expand outward while characters match
    - Track the longest palindrome found
    
    Time Complexity: O(n^2)
    Space Complexity: O(1)
    """
    if not s:
        return ""
    
    def expand_around_center(left: int, right: int) -> tuple:
        """Expand around center and return (start, end) of palindrome"""
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        # Return the valid palindrome boundaries
        return left + 1, right - 1
    
    start = 0
    end = 0
    
    for i in range(len(s)):
        # Case 1: Odd-length palindromes (single character center)
        left1, right1 = expand_around_center(i, i)
        
        # Case 2: Even-length palindromes (center between two characters)
        left2, right2 = expand_around_center(i, i + 1)
        
        # Update if we found a longer palindrome
        if right1 - left1 > end - start:
            start, end = left1, right1
        
        if right2 - left2 > end - start:
            start, end = left2, right2
    
    return s[start:end + 1]
