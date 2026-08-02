def merge_intervals(intervals):
    """
    Merge overlapping intervals in a list of [start, end] pairs.
    Returns merged intervals sorted by start.
    Adjacent intervals (end == next start) are also merged.
    """
    if not intervals:
        return []
    
    # Sort intervals by start time
    intervals.sort(key=lambda x: x[0])
    
    merged = []
    current_start, current_end = intervals[0]
    
    for interval in intervals[1:]:
        start, end = interval
        
        # If current interval overlaps with or is adjacent to the next interval
        if start <= current_end:
            # Merge: update current_end to the maximum of the two ends
            current_end = max(current_end, end)
        else:
            # No overlap, add current interval to merged list
            merged.append([current_start, current_end])
            # Start a new current interval
            current_start, current_end = start, end
    
    # Add the last interval
    merged.append([current_start, current_end])
    
    return merged