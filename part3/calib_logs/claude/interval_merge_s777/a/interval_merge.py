def merge_intervals(intervals):
    """
    Merges all overlapping intervals in a list of [start, end] pairs.
    Adjacent intervals (end == next start) merge.
    Returns the merged intervals sorted by start.
    
    Args:
        intervals: List of [start, end] pairs
        
    Returns:
        List of merged [start, end] pairs sorted by start
    """
    if not intervals:
        return []
    
    # Sort intervals by start time, and by end time if starts are equal
    sorted_intervals = sorted(intervals, key=lambda x: (x[0], x[1]))
    
    # Initialize merged list with the first interval
    merged = [sorted_intervals[0]]
    
    # Iterate through remaining intervals
    for current in sorted_intervals[1:]:
        last_merged = merged[-1]
        
        # If current interval overlaps or is adjacent to the last merged interval
        if current[0] <= last_merged[1]:
            # Merge by extending the end of the last merged interval
            last_merged[1] = max(last_merged[1], current[1])
        else:
            # No overlap, add current interval as a new merged interval
            merged.append(current)
    
    return merged
