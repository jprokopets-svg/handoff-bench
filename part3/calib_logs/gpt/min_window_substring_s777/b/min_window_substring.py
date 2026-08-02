from collections import Counter, defaultdict


def min_window(s: str, t: str) -> str:
    """Return the minimum window substring of s that contains all characters of t (including duplicates).
    If no such window exists, return an empty string.
    """
    if not s or not t:
        return ""

    dict_t = Counter(t)
    required = len(dict_t)

    # left and right pointers
    l, r = 0, 0
    formed = 0
    window_counts = defaultdict(int)

    # ans tuple of the form (window length, left, right)
    ans = (float('inf'), None, None)

    while r < len(s):
        character = s[r]
        window_counts[character] += 1

        # If the current character's count matches the required count in t, increment formed
        if character in dict_t and window_counts[character] == dict_t[character]:
            formed += 1

        # Try and contract the window till the point it ceases to be 'desirable'
        while l <= r and formed == required:
            character = s[l]

            # Save the smallest window until now.
            if r - l + 1 < ans[0]:
                ans = (r - l + 1, l, r)

            # The character at the position pointed by the `l` pointer is no longer a part of the window.
            window_counts[character] -= 1
            if character in dict_t and window_counts[character] < dict_t[character]:
                formed -= 1

            l += 1

        # Keep expanding the window once we are done contracting.
        r += 1

    return "" if ans[0] == float('inf') else s[ans[1] : ans[2] + 1]
