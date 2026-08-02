def length_of_longest_substring(s: str) -> int:
    """
    Return the length of the longest substring without repeating characters.
    
    Args:
        s: Input string
        
    Returns:
        Length of longest substring without repeating characters
    """
    if not s:
        return 0
    
    char_index = {}  # Store the last index of each character
    max_length = 0
    start = 0  # Start of current substring
    
    for i, char in enumerate(s):
        # If character is already in current substring, move start
        if char in char_index and char_index[char] >= start:
            start = char_index[char] + 1
        
        # Update character's last seen index
        char_index[char] = i
        
        # Update max length
        current_length = i - start + 1
        if current_length > max_length:
            max_length = current_length
    
    return max_length