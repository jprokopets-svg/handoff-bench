from collections import Counter, defaultdict


def min_window(s: str, t: str) -> str:
    """Return the minimum window substring of s that contains all chars of t (with duplicates).
    If no such window exists, return an empty string.
    """
    if not t or not s:
        return ''
    if len(t) > len(s):
        return ''

    need = Counter(t)
    required = len(need)

    # window counts
    window_counts = defaultdict(int)
    formed = 0

    l = 0
    r = 0

    min_len = float('inf')
    min_left = 0

    while r < len(s):
        char = s[r]
        window_counts[char] += 1

        if char in need and window_counts[char] == need[char]:
            formed += 1

        # Try and contract the window till the point it ceases to be 'desirable'.
        while l <= r and formed == required:
            char = s[l]

            # Save the smallest window until now.
            if r - l + 1 < min_len:
                min_len = r - l + 1
                min_left = l

            # The character at the position pointed by the `left` pointer is no longer a part of the window.
            window_counts[char] -= 1
            if char in need and window_counts[char] < need[char]:
                formed -= 1

            l += 1

        r += 1

    if min_len == float('inf'):
        return ''
    return s[min_left:min_left + min_len]
