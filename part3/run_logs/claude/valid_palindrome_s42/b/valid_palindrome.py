def valid_palindrome(s: str) -> bool:
    """
    Check if a string is a palindrome, ignoring non-alphanumeric characters and case.
    
    Args:
        s: The string to check
        
    Returns:
        True if the string is a palindrome (ignoring non-alphanumeric characters and case),
        False otherwise
        
    Examples:
        >>> valid_palindrome('A man, a plan, a canal: Panama')
        True
        >>> valid_palindrome('race a car')
        False
        >>> valid_palindrome(' ')
        True
        >>> valid_palindrome('ab_a')
        True
    """
    # Filter to only alphanumeric characters and convert to lowercase
    filtered = ''.join(char.lower() for char in s if char.isalnum())
    
    # Check if the filtered string equals its reverse
    return filtered == filtered[::-1]
