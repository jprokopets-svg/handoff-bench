def merge_intervals(intervals):
    """Merge overlapping or adjacent intervals.

    intervals: list of [start, end]
    returns: list of merged intervals sorted by start
    """
    if not intervals:
        return []
    # Sort intervals by start
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = []
    current_start, current_end = sorted_intervals[0]
    for start, end in sorted_intervals[1:]:
        # If overlapping or adjacent (end == next start), merge
        if start <= current_end:
            # extend the current interval
            current_end = max(current_end, end)
        else:
            merged.append([current_start, current_end])
            current_start, current_end = start, end
    # append last
    merged.append([current_start, current_end])
    return merged
