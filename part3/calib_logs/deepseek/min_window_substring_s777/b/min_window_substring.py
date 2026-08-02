def min_window(s: str, t: str) -> str:
    if not s or not t or len(t) > len(s):
        return ""
    
    # Frequency count for t
    t_count = {}
    for char in t:
        t_count[char] = t_count.get(char, 0) + 1
    
    # Number of unique characters in t
    required = len(t_count)
    
    # Window frequency count
    window_count = {}
    
    # Track how many unique characters have met their required count
    formed = 0
    
    # Sliding window pointers and result
    left = 0
    right = 0
    min_len = float('inf')
    min_left = 0
    min_right = 0
    
    while right < len(s):
        # Add character at right pointer to window
        char = s[right]
        window_count[char] = window_count.get(char, 0) + 1
        
        # Check if this character's count now matches requirement
        if char in t_count and window_count[char] == t_count[char]:
            formed += 1
        
        # Try to contract window while it's valid
        while left <= right and formed == required:
            # Update minimum window
            if right - left + 1 < min_len:
                min_len = right - left + 1
                min_left = left
                min_right = right
            
            # Remove character at left pointer from window
            left_char = s[left]
            window_count[left_char] -= 1
            
            # Check if removing this character broke a requirement
            if left_char in t_count and window_count[left_char] < t_count[left_char]:
                formed -= 1
            
            left += 1
        
        # Expand window
        right += 1
    
    return s[min_left:min_right + 1] if min_len != float('inf') else ""