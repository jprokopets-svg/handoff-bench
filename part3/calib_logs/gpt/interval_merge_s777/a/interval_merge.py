def merge_intervals(intervals):
    """Merge overlapping or adjacent intervals.

    Args:
        intervals (list[list[int]]): list of [start, end] intervals

    Returns:
        list[list[int]]: merged intervals sorted by start
    """
    if not intervals:
        return []
    # Sort by start, then end
    sorted_intervals = sorted(intervals, key=lambda x: (x[0], x[1]))
    merged = []
    curr_start, curr_end = sorted_intervals[0]
    for s, e in sorted_intervals[1:]:
        # If overlapping or adjacent (curr_end >= s), merge
        if curr_end >= s:
            # extend the current interval's end if needed
            if e > curr_end:
                curr_end = e
        else:
            merged.append([curr_start, curr_end])
            curr_start, curr_end = s, e
    merged.append([curr_start, curr_end])
    return merged
