def length_of_longest_substring(s):
    """
    Returns the length of the longest substring without repeating characters.
    
    Args:
        s: A string
        
    Returns:
        The length of the longest substring without repeating characters
    """
    if not s:
        return 0
    
    char_index = {}  # Dictionary to store the most recent index of each character
    max_length = 0
    left = 0  # Left pointer of the sliding window
    
    for right in range(len(s)):
        # If character is already in the current window
        if s[right] in char_index and char_index[s[right]] >= left:
            # Move left pointer to the right of the previous occurrence
            left = char_index[s[right]] + 1
        
        # Update the most recent index of the current character
        char_index[s[right]] = right
        
        # Update max_length with the current window size
        max_length = max(max_length, right - left + 1)
    
    return max_length
