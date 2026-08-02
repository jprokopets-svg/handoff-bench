def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
    
    # Sort intervals by start time, then by end time
    sorted_intervals = sorted(intervals, key=lambda x: (x[0], x[1]))
    
    # Initialize result with the first interval
    merged = [sorted_intervals[0]]
    
    # Iterate through remaining intervals
    for current in sorted_intervals[1:]:
        last_merged = merged[-1]
        
        # Check if current interval overlaps or is adjacent to the last merged interval
        if current[0] <= last_merged[1]:
            # Merge by extending the end of the last merged interval
            last_merged[1] = max(last_merged[1], current[1])
        else:
            # No overlap, add current interval as a new entry
            merged.append(current)
    
    return merged
