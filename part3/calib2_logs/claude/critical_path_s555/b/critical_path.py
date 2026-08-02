def critical_path(durations: dict, deps: list) -> tuple:
    """
    Compute the critical path for a project given task durations and dependencies.
    
    Args:
        durations: dict mapping task id -> duration
        deps: list of (a, b) tuples meaning task a must complete before task b starts
    
    Returns:
        (project_duration, critical_path_list) where:
        - project_duration is the minimum time to complete all tasks
        - critical_path_list is a list of task ids on one longest path from source to sink
    
    Raises:
        ValueError: if the dependency graph contains a cycle
    """
    # Handle empty input
    if not durations:
        return (0.0, [])
    
    # Build adjacency list and in-degree map
    graph = {task: [] for task in durations}
    in_degree = {task: 0 for task in durations}
    
    for a, b in deps:
        graph[a].append(b)
        in_degree[b] = in_degree.get(b, 0) + 1
    
    # Kahn's topological sort with cycle detection
    queue = [task for task in durations if in_degree[task] == 0]
    topo_order = []
    temp_in_degree = in_degree.copy()
    
    while queue:
        node = queue.pop(0)
        topo_order.append(node)
        for neighbor in graph[node]:
            temp_in_degree[neighbor] -= 1
            if temp_in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Check for cycle
    if len(topo_order) != len(durations):
        raise ValueError("Dependency graph contains a cycle")
    
    # Compute longest path using dynamic programming
    # dist[task] = longest path ending at task
    dist = {task: durations[task] for task in durations}
    predecessor = {task: None for task in durations}
    
    for task in topo_order:
        for neighbor in graph[task]:
            if dist[task] + durations[neighbor] > dist[neighbor]:
                dist[neighbor] = dist[task] + durations[neighbor]
                predecessor[neighbor] = task
    
    # Find the sink node(s) with maximum distance
    # A sink is a node with no outgoing edges
    sinks = [task for task in durations if not graph[task]]
    
    if not sinks:
        # All tasks are in a cycle (already caught above)
        raise ValueError("Dependency graph contains a cycle")
    
    # Find the sink with maximum distance
    max_sink = max(sinks, key=lambda t: dist[t])
    project_duration = dist[max_sink]
    
    # Reconstruct the critical path by backtracking from sink
    path = []
    current = max_sink
    while current is not None:
        path.append(current)
        current = predecessor[current]
    
    path.reverse()
    
    return (project_duration, path)
