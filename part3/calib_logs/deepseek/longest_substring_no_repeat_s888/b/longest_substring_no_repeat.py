def length_of_longest_substring(s: str) -> int:
    """
    Returns the length of the longest substring without repeating characters.
    
    Uses a sliding window approach with a hash map to track the most recent
    index of each character. Time complexity: O(n), space complexity: O(min(n, m))
    where m is the size of the character set.
    """
    if not s:
        return 0
    
    # Dictionary to store the most recent index of each character
    char_index = {}
    max_length = 0
    start = 0  # Start of the current window
    
    for end, char in enumerate(s):
        # If character is in the dictionary and its index is within the current window
        if char in char_index and char_index[char] >= start:
            # Move the start of the window to the right of the previous occurrence
            start = char_index[char] + 1
        
        # Update the character's most recent index
        char_index[char] = end
        
        # Update the maximum length
        current_length = end - start + 1
        if current_length > max_length:
            max_length = current_length
    
    return max_length