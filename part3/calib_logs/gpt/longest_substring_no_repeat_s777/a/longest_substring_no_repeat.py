def length_of_longest_substring(s: str) -> int:
    """Return the length of the longest substring without repeating characters.

    Uses sliding window with a dictionary to remember the last index of each character.
    """
    last_index = {}
    start = 0
    max_len = 0
    for i, ch in enumerate(s):
        if ch in last_index and last_index[ch] >= start:
            # move start right after the previous occurrence
            start = last_index[ch] + 1
        last_index[ch] = i
        current_len = i - start + 1
        if current_len > max_len:
            max_len = current_len
    return max_len
