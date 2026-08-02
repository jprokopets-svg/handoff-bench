def length_of_longest_substring(s: str) -> int:
    if not s:
        return 0

    max_len = 0
    start = 0
    char_map = {}

    for i, char in enumerate(s):
        if char in char_map and char_map[char] >= start:
            start = char_map[char] + 1
        char_map[char] = i
        max_len = max(max_len, i - start + 1)

    return max_len