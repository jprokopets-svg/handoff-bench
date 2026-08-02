def length_of_longest_substring(s: str) -> int:
    """Return the length of the longest substring without repeating characters."""
    # sliding window with last seen positions
    last = {}
    start = 0
    max_len = 0
    for i, ch in enumerate(s):
        if ch in last and last[ch] >= start:
            # move start to one after last occurrence
            start = last[ch] + 1
        last[ch] = i
        curr_len = i - start + 1
        if curr_len > max_len:
            max_len = curr_len
    return max_len
