def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
    
    # Sort intervals by start time
    intervals.sort(key=lambda x: x[0])
    
    merged = []
    current_start, current_end = intervals[0]
    
    for interval in intervals[1:]:
        start, end = interval
        
        # If intervals overlap or are adjacent (end == start)
        if start <= current_end:
            # Merge intervals by taking the maximum end
            current_end = max(current_end, end)
        else:
            # No overlap, add current interval to merged list
            merged.append([current_start, current_end])
            current_start, current_end = start, end
    
    # Add the last interval
    merged.append([current_start, current_end])
    
    return merged