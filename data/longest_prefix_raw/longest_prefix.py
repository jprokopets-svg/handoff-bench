def longest_common_prefix(strs):
    """
    Find the longest common prefix string among an array of strings.
    Return empty string if none.
    
    Args:
        strs: List of strings
        
    Returns:
        The longest common prefix string, or empty string if none exists
    """
    if not strs:
        return ''
    
    # Handle single string or empty string cases
    if len(strs) == 1:
        return strs[0]
    
    # Find the minimum length among all strings
    min_len = min(len(s) for s in strs)
    
    # Compare characters at each position
    for i in range(min_len):
        char = strs[0][i]
        for j in range(1, len(strs)):
            if strs[j][i] != char:
                return strs[0][:i]
    
    # If we've compared all characters up to min_len, return the prefix
    return strs[0][:min_len]
