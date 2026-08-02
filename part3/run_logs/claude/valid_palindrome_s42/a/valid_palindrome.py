def valid_palindrome(s):
    """
    Returns True if a string is a palindrome, ignoring non-alphanumeric characters and case.
    
    Args:
        s: A string to check
        
    Returns:
        True if the string is a palindrome (ignoring non-alphanumeric characters and case), False otherwise
    """
    # Filter to keep only alphanumeric characters and convert to lowercase
    filtered = ''.join(char.lower() for char in s if char.isalnum())
    
    # Check if the filtered string is equal to its reverse
    return filtered == filtered[::-1]
