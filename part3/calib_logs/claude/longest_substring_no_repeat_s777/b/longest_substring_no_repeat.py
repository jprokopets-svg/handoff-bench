def length_of_longest_substring(s: str) -> int:
    """
    Returns the length of the longest substring without repeating characters.
    
    Uses a sliding window approach with character index tracking.
    Time Complexity: O(n)
    Space Complexity: O(min(n, charset_size))
    
    Args:
        s: Input string
        
    Returns:
        Length of the longest substring without repeating characters
        
    Examples:
        >>> length_of_longest_substring('abcabcbb')
        3
        >>> length_of_longest_substring('bbbbb')
        1
        >>> length_of_longest_substring('pwwkew')
        3
        >>> length_of_longest_substring('')
        0
    """
    if not s:
        return 0
    
    char_index = {}  # Dictionary to store the last seen index of each character
    max_length = 0
    start = 0  # Left pointer of the sliding window
    
    for end in range(len(s)):
        char = s[end]
        
        # If character is already in the current window, move start pointer
        if char in char_index and char_index[char] >= start:
            start = char_index[char] + 1
        
        # Update the last seen index of the character
        char_index[char] = end
        
        # Update max length
        max_length = max(max_length, end - start + 1)
    
    return max_length
