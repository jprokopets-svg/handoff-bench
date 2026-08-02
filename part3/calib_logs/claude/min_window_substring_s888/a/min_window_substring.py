def min_window(s, t):
    """
    Returns the minimum window substring of s that contains all characters of t (including duplicates).
    Returns '' if no such window exists.
    
    Args:
        s: The string to search in
        t: The string containing characters we need to find
        
    Returns:
        The minimum window substring, or '' if no valid window exists
    """
    if not s or not t:
        return ''
    
    # Dictionary to keep track of characters in t and their frequencies
    dict_t = {}
    for char in t:
        dict_t[char] = dict_t.get(char, 0) + 1
    
    required = len(dict_t)  # Number of unique characters in t that need to be present
    
    # Left and right pointers
    l, r = 0, 0
    
    # formed is used to keep track of how many unique characters in t are present in current window with desired frequency
    formed = 0
    
    # Dictionary to keep track of characters in current window
    window_counts = {}
    
    # ans tuple of the form (window length, left, right)
    ans = float('inf'), None, None
    
    while r < len(s):
        # Add one character from the right to the window
        character = s[r]
        window_counts[character] = window_counts.get(character, 0) + 1
        
        # If the frequency of the current character added equals to the desired count in t then increment the formed count
        if character in dict_t and window_counts[character] == dict_t[character]:
            formed += 1
        
        # Try to contract the window until the point where it ceases to be 'desirable'
        while l <= r and formed == required:
            character = s[l]
            
            # Save the smallest window until now
            if r - l + 1 < ans[0]:
                ans = (r - l + 1, l, r)
            
            # The character at the position pointed by the `left` pointer is no longer a part of the window
            window_counts[character] -= 1
            if character in dict_t and window_counts[character] < dict_t[character]:
                formed -= 1
            
            # Move the left pointer ahead for the next iteration
            l += 1
        
        # Keep expanding the window by moving right pointer
        r += 1
    
    # Return the smallest window or '' if no such window exists
    return '' if ans[0] == float('inf') else s[ans[1]:ans[2] + 1]
