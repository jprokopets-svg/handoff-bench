from collections import Counter


def min_window(s: str, t: str) -> str:
    """Return the minimum window substring of s that contains all characters of t.

    If no such window exists, return empty string.
    """
    if not t or not s:
        return "" if t else ""

    dict_t = Counter(t)
    required = len(dict_t)  # number of unique chars required

    # left and right pointers
    l, r = 0, 0
    formed = 0
    window_counts = {}

    # answer tuple (window length, left, right)
    ans = (float('inf'), None, None)

    while r < len(s):
        character = s[r]
        window_counts[character] = window_counts.get(character, 0) + 1

        # check if current char added satisfies a required character
        if character in dict_t and window_counts[character] == dict_t[character]:
            formed += 1

        # try and contract the window till the point it ceases to be 'desirable'
        while l <= r and formed == required:
            character = s[l]

            # save the smallest window until now
            if r - l + 1 < ans[0]:
                ans = (r - l + 1, l, r)

            # the character at the position pointed by the `l` pointer is no longer a part of the window
            window_counts[character] -= 1
            if character in dict_t and window_counts[character] < dict_t[character]:
                formed -= 1

            l += 1

        # keep expanding the window once we are done contracting
        r += 1

    return "" if ans[0] == float('inf') else s[ans[1]:ans[2]+1]
