def word_break(s, word_dict):
    """
    Determine if a string can be segmented into space-separated words from a dictionary.
    
    Args:
        s: The string to segment
        word_dict: A list or set of valid words
    
    Returns:
        True if the string can be segmented into words from the dictionary, False otherwise
    """
    if not s:
        return True
    
    # Convert to set for O(1) lookup
    word_set = set(word_dict)
    
    # dp[i] represents whether s[0:i] can be segmented
    dp = [False] * (len(s) + 1)
    dp[0] = True  # Empty string can always be segmented
    
    for i in range(1, len(s) + 1):
        for j in range(i):
            # If s[0:j] can be segmented and s[j:i] is a valid word
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    
    return dp[len(s)]
