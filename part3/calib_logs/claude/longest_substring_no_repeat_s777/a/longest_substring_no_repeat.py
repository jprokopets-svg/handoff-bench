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
    
    char_index = {}  # Dictionary to store the last seen index of each character
    max_length = 0
    start = 0  # Start of the current window
    
    for end in range(len(s)):
        char = s[end]
        
        # If character is already in the current window, move start pointer
        if char in char_index and char_index[char] >= start:
            start = char_index[char] + 1
        
        # Update the last seen index of the character
        char_index[char] = end
        
        # Update max_length
        max_length = max(max_length, end - start + 1)
    
    return max_length
