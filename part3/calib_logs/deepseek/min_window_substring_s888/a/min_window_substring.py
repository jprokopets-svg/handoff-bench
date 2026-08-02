def min_window(s: str, t: str) -> str:
    """
    Returns the minimum window substring of s that contains all characters of t
    (including duplicates). Returns '' if no such window exists.
    """
    if not s or not t or len(t) > len(s):
        return ""
    
    from collections import Counter
    
    # Count characters in t
    t_count = Counter(t)
    required = len(t_count)
    
    # Sliding window variables
    left = 0
    formed = 0
    window_counts = {}
    
    # Result variables
    min_len = float('inf')
    min_left = 0
    
    for right in range(len(s)):
        char = s[right]
        
        # Add character to window
        window_counts[char] = window_counts.get(char, 0) + 1
        
        # Check if this character completes a requirement
        if char in t_count and window_counts[char] == t_count[char]:
            formed += 1
        
        # Try to contract window while it's valid
        while left <= right and formed == required:
            # Update minimum window
            if right - left + 1 < min_len:
                min_len = right - left + 1
                min_left = left
            
            # Remove left character from window
            left_char = s[left]
            window_counts[left_char] -= 1
            
            # Check if removing this character broke a requirement
            if left_char in t_count and window_counts[left_char] < t_count[left_char]:
                formed -= 1
            
            left += 1
    
    return "" if min_len == float('inf') else s[min_left:min_left + min_len]