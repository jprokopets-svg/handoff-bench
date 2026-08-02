def length_of_longest_substring(s: str) -> int:
    """
    Returns the length of the longest substring without repeating characters.
    
    Uses a sliding window approach with a dictionary to track character positions.
    
    Time Complexity: O(n) where n is the length of the string
    Space Complexity: O(min(n, m)) where m is the size of the character set
    
    Examples:
        >>> length_of_longest_substring('abcabcbb')
        3  # "abc"
        >>> length_of_longest_substring('bbbbb')
        1  # "b"
        >>> length_of_longest_substring('pwwkew')
        3  # "wke"
        >>> length_of_longest_substring('')
        0
        >>> length_of_longest_substring('au')
        2  # "au"
        >>> length_of_longest_substring('dvdf')
        3  # "vdf"
    """
    if not s:
        return 0
    
    # Dictionary to store the most recent index of each character
    char_index = {}
    max_length = 0
    left = 0  # Left pointer of the sliding window
    
    for right in range(len(s)):
        # If character is already in current window, move left pointer
        if s[right] in char_index and char_index[s[right]] >= left:
            left = char_index[s[right]] + 1
        
        # Update the most recent index of the current character
        char_index[s[right]] = right
        
        # Update max length
        max_length = max(max_length, right - left + 1)
    
    return max_length
