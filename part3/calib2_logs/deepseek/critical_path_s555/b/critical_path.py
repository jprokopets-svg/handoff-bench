def critical_path(durations: dict, deps: list) -> tuple:
    # Handle empty durations
    if not durations:
        return (0.0, [])
    
    # Build adjacency list and indegree/outdegree counts
    adj = {task: [] for task in durations}
    indegree = {task: 0 for task in durations}
    outdegree = {task: 0 for task in durations}
    
    for a, b in deps:
        if a not in adj:
            adj[a] = []
        if b not in adj:
            adj[b] = []
        adj[a].append(b)
        indegree[b] += 1
        outdegree[a] += 1
    
    # Initialize all tasks
    tasks = list(durations.keys())
    
    # Topological sort with cycle detection
    indegree_copy = indegree.copy()
    queue = [task for task in tasks if indegree_copy[task] == 0]
    topo_order = []
    
    while queue:
        task = queue.pop(0)
        topo_order.append(task)
        for neighbor in adj.get(task, []):
            indegree_copy[neighbor] -= 1
            if indegree_copy[neighbor] == 0:
                queue.append(neighbor)
    
    # Check for cycle
    if len(topo_order) != len(tasks):
        raise ValueError("Cycle detected")
    
    # Forward pass: compute earliest start times
    earliest_start = {task: 0.0 for task in tasks}
    for task in topo_order:
        for neighbor in adj.get(task, []):
            earliest_start[neighbor] = max(
                earliest_start[neighbor],
                earliest_start[task] + durations[task]
            )
    
    # Project duration is max of earliest finish times
    project_duration = max(
        earliest_start[task] + durations[task] for task in tasks
    )
    
    # Backward pass: compute latest start times
    latest_start = {task: float('inf') for task in tasks}
    # Initialize sink tasks (no outgoing edges)
    for task in tasks:
        if outdegree[task] == 0:
            latest_start[task] = project_duration - durations[task]
    
    # Process in reverse topological order
    for task in reversed(topo_order):
        # Update predecessors
        for pred in tasks:
            if task in adj.get(pred, []):
                latest_start[pred] = min(
                    latest_start[pred],
                    latest_start[task] - durations[pred]
                )
    
    # Find critical path: tasks where earliest_start == latest_start
    # and form a continuous path from source to sink
    critical_tasks = {
        task for task in tasks 
        if abs(earliest_start[task] - latest_start[task]) < 1e-9
    }
    
    # Build the critical path from source to sink
    # Find source critical tasks (indegree 0 or all predecessors not critical)
    source_critical = []
    for task in critical_tasks:
        is_source = True
        for pred in tasks:
            if task in adj.get(pred, []) and pred in critical_tasks:
                is_source = False
                break
        if is_source:
            source_critical.append(task)
    
    # Start from a source critical task and follow critical successors
    if not source_critical:
        # If no obvious source, start from any critical task
        # that has earliest_start = 0
        for task in critical_tasks:
            if abs(earliest_start[task]) < 1e-9:
                source_critical.append(task)
                break
    
    if not source_critical:
        # Fallback: use first critical task
        source_critical.append(next(iter(critical_tasks)))
    
    # Build path from source to sink
    path = []
    current = source_critical[0]
    visited = set()
    
    while current and current not in visited:
        visited.add(current)
        path.append(current)
        
        # Find critical successor
        next_task = None
        for neighbor in adj.get(current, []):
            if neighbor in critical_tasks:
                next_task = neighbor
                break
        
        current = next_task
    
    # Verify path sum equals project duration
    path_duration = sum(durations[task] for task in path)
    if abs(path_duration - project_duration) > 1e-9:
        # If path doesn't match, try to find a better path
        # by exploring all possible critical paths
        def dfs_find_path(current, current_path, current_sum):
            if outdegree[current] == 0:
                if abs(current_sum - project_duration) < 1e-9:
                    return current_path
                return None
            
            for neighbor in adj.get(current, []):
                if neighbor in critical_tasks:
                    result = dfs_find_path(
                        neighbor, 
                        current_path + [neighbor],
                        current_sum + durations[neighbor]
                    )
                    if result:
                        return result
            return None
        
        # Try from each source critical task
        for source in source_critical:
            result = dfs_find_path(source, [source], durations[source])
            if result:
                path = result
                break
    
    return (project_duration, path)