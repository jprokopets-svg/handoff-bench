def min_window(s: str, t: str) -> str:
    """
    Returns the minimum window substring of s that contains all characters of t
    (including duplicates). Returns '' if no such window exists.
    """
    if not s or not t:
        return ""
    
    # Frequency map for characters in t
    t_count = {}
    for char in t:
        t_count[char] = t_count.get(char, 0) + 1
    
    # Variables for sliding window
    left = 0
    min_len = float('inf')
    min_start = 0
    required = len(t_count)  # Number of unique characters we need to match
    formed = 0  # Number of unique characters we've matched so far
    
    # Frequency map for current window
    window_count = {}
    
    for right in range(len(s)):
        char = s[right]
        window_count[char] = window_count.get(char, 0) + 1
        
        # Check if this character completes a requirement
        if char in t_count and window_count[char] == t_count[char]:
            formed += 1
        
        # Try to shrink the window while it's valid
        while left <= right and formed == required:
            # Update minimum window
            if right - left + 1 < min_len:
                min_len = right - left + 1
                min_start = left
            
            # Remove left character from window
            left_char = s[left]
            window_count[left_char] -= 1
            
            # Check if removing this character broke a requirement
            if left_char in t_count and window_count[left_char] < t_count[left_char]:
                formed -= 1
            
            left += 1
    
    return "" if min_len == float('inf') else s[min_start:min_start + min_len]