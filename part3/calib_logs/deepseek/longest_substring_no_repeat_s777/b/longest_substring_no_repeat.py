def length_of_longest_substring(s: str) -> int:
    """
    Return the length of the longest substring without repeating characters.
    
    Uses a sliding window approach with a set to track characters in the current window.
    """
    if not s:
        return 0
    
    char_set = set()
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        # If current character is already in the window, move left pointer
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        
        # Add current character to the window
        char_set.add(s[right])
        
        # Update max length
        max_length = max(max_length, right - left + 1)
    
    return max_length