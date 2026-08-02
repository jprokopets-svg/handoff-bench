from typing import List


def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:
    """Merge overlapping or adjacent intervals and return merged intervals sorted by start.

    Adjacent intervals where end == next_start are merged.
    """
    if not intervals:
        return []

    # Sort by start
    sorted_intervals = sorted(intervals, key=lambda x: x[0])

    merged: List[List[int]] = []
    current_start, current_end = sorted_intervals[0]

    for start, end in sorted_intervals[1:]:
        if start <= current_end:  # overlap or adjacent
            # merge
            current_end = max(current_end, end)
        else:
            merged.append([current_start, current_end])
            current_start, current_end = start, end

    merged.append([current_start, current_end])
    return merged
