from collections import Counter, defaultdict


def min_window(s: str, t: str) -> str:
    """Return the minimum window in s which will contain all the characters in t.

    If there is no such window, return the empty string "".
    """
    if not s or not t or len(t) > len(s):
        return ""

    required_counts = Counter(t)
    window_counts = defaultdict(int)

    required = len(required_counts)
    formed = 0

    l = 0
    ans_len = float('inf')
    ans_left = 0

    # Expand the window with r
    for r, ch in enumerate(s):
        window_counts[ch] += 1

        # If current character's count matches the required count, increment formed
        if ch in required_counts and window_counts[ch] == required_counts[ch]:
            formed += 1

        # Try and contract the window till the point it ceases to be 'desirable'
        while l <= r and formed == required:
            # Update smallest window
            window_size = r - l + 1
            if window_size < ans_len:
                ans_len = window_size
                ans_left = l

            # The character at the position l is going to be removed from window
            left_ch = s[l]
            window_counts[left_ch] -= 1
            if left_ch in required_counts and window_counts[left_ch] < required_counts[left_ch]:
                formed -= 1

            l += 1

    if ans_len == float('inf'):
        return ""
    return s[ans_left:ans_left + ans_len]
