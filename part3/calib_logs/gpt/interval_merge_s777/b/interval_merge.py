from typing import List


def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:
    """Merge overlapping or adjacent intervals.

    Args:
        intervals: list of [start, end] pairs

    Returns:
        merged list of intervals sorted by start
    """
    if not intervals:
        return []

    # Sort by start then end
    sorted_intervals = sorted(intervals, key=lambda x: (x[0], x[1]))

    merged: List[List[int]] = []
    for interval in sorted_intervals:
        # Expect interval to be an indexable of length >= 2
        if not merged:
            merged.append([interval[0], interval[1]])
            continue

        last = merged[-1]
        curr_start, curr_end = interval[0], interval[1]

        # If overlapping or adjacent (last_end >= curr_start), merge
        if last[1] >= curr_start:
            last[1] = max(last[1], curr_end)
        else:
            merged.append([curr_start, curr_end])

    return merged
