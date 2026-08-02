def length_of_longest_substring(s: str) -> int:
    """Return the length of the longest substring without repeating characters.

    Uses a sliding-window approach with a dictionary that maps each character
    to its last seen index. Move the start of the window forward when a
    repeated character is found inside the current window.

    Time complexity: O(n)
    Space complexity: O(min(n, charset_size))

    Note: This function treats Python string elements (code points). It does
    not perform grapheme-cluster normalization.
    """
    if not s:
        return 0

    last_index = {}
    start = 0
    max_len = 0

    for i, ch in enumerate(s):
        if ch in last_index and last_index[ch] >= start:
            # move start just after the previous occurrence
            start = last_index[ch] + 1
        last_index[ch] = i
        curr_len = i - start + 1
        if curr_len > max_len:
            max_len = curr_len

    return max_len
