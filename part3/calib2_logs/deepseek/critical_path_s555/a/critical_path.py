from collections import defaultdict, deque


def critical_path(durations, dependencies):
    """
    Compute the critical path in a task dependency graph.
    
    Args:
        durations: dict mapping task id -> duration (float)
        dependencies: list of (a, b) meaning task a must complete before b can start
    
    Returns:
        tuple (project_duration, critical_path) where critical_path is a list
        of task ids on one longest path from source to sink.
    
    Raises:
        ValueError: if dependency graph contains a cycle
    """
    # Empty durations case
    if not durations:
        return (0.0, [])
    
    # Build adjacency list and indegree count
    adj = defaultdict(list)
    indegree = defaultdict(int)
    for a, b in dependencies:
        adj[a].append(b)
        indegree[b] = indegree.get(b, 0) + 1
        # Ensure all tasks appear in indegree dict
        indegree[a] = indegree.get(a, 0)
    
    # Initialize indegree for tasks with no dependencies
    for task in durations:
        if task not in indegree:
            indegree[task] = 0
    
    # Topological sort with cycle detection
    zero_indegree = deque([task for task in durations if indegree[task] == 0])
    topo_order = []
    
    while zero_indegree:
        task = zero_indegree.popleft()
        topo_order.append(task)
        for neighbor in adj[task]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                zero_indegree.append(neighbor)
    
    # Check for cycle
    if len(topo_order) != len(durations):
        raise ValueError("Dependency graph contains a cycle")
    
    # Forward pass: compute earliest start times
    earliest_start = {task: 0.0 for task in durations}
    for task in topo_order:
        for neighbor in adj[task]:
            earliest_start[neighbor] = max(
                earliest_start[neighbor],
                earliest_start[task] + durations[task]
            )
    
    # Project duration is max of earliest finish times
    project_duration = max(
        earliest_start[task] + durations[task] for task in durations
    )
    
    # Backward pass: compute latest start times
    latest_start = {task: project_duration - durations[task] for task in durations}
    for task in reversed(topo_order):
        for neighbor in adj[task]:
            latest_start[task] = min(
                latest_start[task],
                latest_start[neighbor] - durations[task]
            )
    
    # Find critical tasks (where earliest_start == latest_start)
    critical_tasks = {
        task for task in durations
        if abs(earliest_start[task] - latest_start[task]) < 1e-9
    }
    
    # Build critical path from source to sink
    # Find source tasks (no incoming edges) that are critical
    sources = [task for task in durations if task not in indegree or indegree[task] == 0]
    critical_sources = [task for task in sources if task in critical_tasks]
    
    if not critical_sources:
        # No critical source found, try to find any critical task
        if critical_tasks:
            start_task = next(iter(critical_tasks))
        else:
            # No critical tasks, return any path
            start_task = topo_order[0]
    else:
        start_task = critical_sources[0]
    
    # Follow critical tasks to build path
    path = [start_task]
    current = start_task
    
    while True:
        # Find critical successors
        critical_successors = [
            neighbor for neighbor in adj[current]
            if neighbor in critical_tasks
        ]
        
        if not critical_successors:
            break
        
        # Choose one critical successor (prefer the one with larger duration for tie-breaking)
        next_task = max(critical_successors, key=lambda t: durations[t])
        path.append(next_task)
        current = next_task
    
    return (project_duration, path)