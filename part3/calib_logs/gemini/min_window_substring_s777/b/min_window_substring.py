
def min_window(s: str, t: str) -> str:
    if not t:
        return ""

    dict_t = {}
    for char in t:
        dict_t[char] = dict_t.get(char, 0) + 1

    window_start = 0
    matched = 0
    min_length = float('inf')
    substring_start = 0

    for window_end in range(len(s)):
        right_char = s[window_end]

        if right_char in dict_t:
            dict_t[right_char] -= 1
            if dict_t[right_char] >= 0:  # Only count as matched if we still need this char or have exactly enough
                matched += 1

        while matched == len(t):  # Check if all characters in t are in the current window
            if (window_end - window_start + 1) < min_length:
                min_length = (window_end - window_start + 1)
                substring_start = window_start

            left_char = s[window_start]
            window_start += 1

            if left_char in dict_t:
                if dict_t[left_char] == 0:  # If we are removing a character that was exactly matched
                    matched -= 1
                dict_t[left_char] += 1

    if min_length == float('inf'):
        return ""
    return s[substring_start:substring_start + min_length]
