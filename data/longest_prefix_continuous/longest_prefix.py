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
    
    # Handle single string or empty string cases
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
                # Mismatch found, return prefix up to this point
                return strings[0][:i]
    
    # All characters matched up to min_length
    return strings[0][:min_length]
