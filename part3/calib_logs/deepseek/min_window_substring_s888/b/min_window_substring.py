from collections import Counter

def min_window(s: str, t: str) -> str:
    if not s or not t or len(s) < len(t):
        return ""
    
    # Count characters in t
    t_counts = Counter(t)
    required = len(t_counts)  # number of unique characters we need to match
    
    # Window state
    window_counts = {}
    formed = 0  # number of unique characters in window that meet t's requirements
    
    # Result tracking
    min_len = float('inf')
    min_left = min_right = 0
    
    left = 0
    for right in range(len(s)):
        char = s[right]
        
        # Add character to window
        if char in t_counts:
            window_counts[char] = window_counts.get(char, 0) + 1
            
            # Check if this character's count now matches t's requirement
            if window_counts[char] == t_counts[char]:
                formed += 1
        
        # Try to contract window while all requirements are met
        while formed == required and left <= right:
            # Update minimum window
            window_len = right - left + 1
            if window_len < min_len:
                min_len = window_len
                min_left = left
                min_right = right
            
            # Remove left character from window
            left_char = s[left]
            if left_char in t_counts:
                window_counts[left_char] -= 1
                if window_counts[left_char] < t_counts[left_char]:
                    formed -= 1
            left += 1
    
    return s[min_left:min_right + 1] if min_len != float('inf') else ""