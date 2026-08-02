from collections import Counter

def min_window(s: str, t: str) -> str:
    if not t:
        return ""

    dict_t = Counter(t)
    window_start = 0
    matched = 0
    min_length = float('inf')
    substring_start = 0

    for window_end in range(len(s)):
        char = s[window_end]
        if char in dict_t:
            dict_t[char] -= 1
            if dict_t[char] >= 0:
                matched += 1

        while matched == len(t):
            if window_end - window_start + 1 < min_length:
                min_length = window_end - window_start + 1
                substring_start = window_start

            char_to_remove = s[window_start]
            window_start += 1
            if char_to_remove in dict_t:
                if dict_t[char_to_remove] >= 0:
                    matched -= 1
                dict_t[char_to_remove] += 1

    if min_length == float('inf'):
        return ""
    return s[substring_start : substring_start + min_length]
