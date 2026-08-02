def valid_palindrome(s: str) -> bool:
    """
    Check if a string is a palindrome, ignoring non-alphanumeric characters and case.
    
    Args:
        s: Input string to check
        
    Returns:
        True if the string is a palindrome (ignoring non-alphanumeric chars and case),
        False otherwise
    """
    left = 0
    right = len(s) - 1
    
    while left < right:
        # Skip non-alphanumeric characters from left
        while left < right and not s[left].isalnum():
            left += 1
        
        # Skip non-alphanumeric characters from right
        while left < right and not s[right].isalnum():
            right -= 1
        
        # Compare characters (case-insensitive)
        if left < right and s[left].lower() != s[right].lower():
            return False
        
        left += 1
        right -= 1
    
    return True