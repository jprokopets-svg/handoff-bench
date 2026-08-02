def critical_path(durations: dict, deps: list) -> tuple:
    # Empty durations case
    if not durations:
        return (0.0, [])
    
    # Validate all tasks in dependencies exist in durations
    all_tasks = set(durations.keys())
    for a, b in deps:
        if a not in all_tasks:
            raise ValueError(f"Task {a} in dependencies not found in durations")
        if b not in all_tasks:
            raise ValueError(f"Task {b} in dependencies not found in durations")
    
    # Build adjacency list and indegree count
    adj = {task: [] for task in all_tasks}
    indegree = {task: 0 for task in all_tasks}
    for a, b in deps:
        adj[a].append(b)
        indegree[b] += 1
    
    # Topological sort (Kahn's algorithm) for cycle detection
    zero_indegree = [task for task in all_tasks if indegree[task] == 0]
    topo_order = []
    
    while zero_indegree:
        task = zero_indegree.pop()
        topo_order.append(task)
        for neighbor in adj[task]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                zero_indegree.append(neighbor)
    
    # If not all tasks were processed, there's a cycle
    if len(topo_order) != len(all_tasks):
        raise ValueError("Dependency graph contains a cycle")
    
    # Forward pass: compute earliest start times
    earliest_start = {task: 0.0 for task in all_tasks}
    for task in topo_order:
        for neighbor in adj[task]:
            earliest_start[neighbor] = max(
                earliest_start[neighbor],
                earliest_start[task] + durations[task]
            )
    
    # Project duration is max of earliest_start + duration
    project_duration = 0.0
    for task in all_tasks:
        project_duration = max(
            project_duration,
            earliest_start[task] + durations[task]
        )
    
    # Backward pass: compute latest start times
    latest_start = {task: float('inf') for task in all_tasks}
    # Initialize sinks (tasks with no outgoing edges)
    for task in all_tasks:
        if not adj[task]:  # sink task
            latest_start[task] = project_duration - durations[task]
    
    # Process in reverse topological order
    for task in reversed(topo_order):
        # For each predecessor (we need reverse adjacency)
        # But we can compute from successors since we have forward adjacency
        for successor in adj[task]:
            latest_start[task] = min(
                latest_start[task],
                latest_start[successor] - durations[task]
            )
        # If still infinity (no successors), it's a sink already handled
    
    # Identify critical tasks: earliest_start == latest_start
    critical_tasks = {
        task for task in all_tasks
        if abs(earliest_start[task] - latest_start[task]) < 1e-9
    }
    
    # Find a critical source (critical task with no critical predecessors)
    # Build critical adjacency
    critical_adj = {task: [] for task in critical_tasks}
    for a, b in deps:
        if a in critical_tasks and b in critical_tasks:
            critical_adj[a].append(b)
    
    # Find critical sources (no incoming critical edges)
    critical_sources = set(critical_tasks)
    for a, b in deps:
        if b in critical_tasks and a in critical_tasks:
            critical_sources.discard(b)
    
    # Start from a critical source and follow critical path
    if not critical_sources:
        # Should not happen if there's at least one critical task
        # But handle edge case
        return (project_duration, [])
    
    # Reconstruct one critical path
    path = []
    current = next(iter(critical_sources))  # take any critical source
    
    while current in critical_tasks:
        path.append(current)
        # Find a critical successor
        next_task = None
        for succ in critical_adj[current]:
            if succ in critical_tasks:
                next_task = succ
                break
        if next_task is None:
            break
        current = next_task
    
    return (project_duration, path)