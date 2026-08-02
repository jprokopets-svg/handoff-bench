from typing import Dict


def length_of_longest_substring(s: str) -> int:
    """Return length of the longest substring without repeating characters.

    Uses a sliding-window approach with a dictionary that maps characters to
    their last-seen index. Time complexity O(n), space O(min(n, charset)).
    """
    last_seen: Dict[str, int] = {}
    start = 0
    max_len = 0

    for i, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= start:
            # move start to one past the previous occurrence of ch
            start = last_seen[ch] + 1
        last_seen[ch] = i
        current_len = i - start + 1
        if current_len > max_len:
            max_len = current_len

    return max_len
