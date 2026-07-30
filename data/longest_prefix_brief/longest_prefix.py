def longest_common_prefix(strings):
    """
    Find the longest common prefix string among an array of strings.
    Return empty string if none.
    
    Args:
        strings: List of strings
        
    Returns:
        The longest common prefix string, or empty string if none
    """
    if not strings:
        return ''
    
    # If there's only one string, return it
    if len(strings) == 1:
        return strings[0]
    
    # Find the minimum length among all strings
    min_length = min(len(s) for s in strings)
    
    # Compare characters at each position
    for i in range(min_length):
        # Get the character at position i from the first string
        char = strings[0][i]
        
        # Check if all strings have the same character at position i
        for s in strings[1:]:
            if s[i] != char:
                # If any string has a different character, return prefix up to i
                return strings[0][:i]
    
    # If we've gone through all positions without finding a mismatch,
    # the common prefix is the first min_length characters
    return strings[0][:min_length]
