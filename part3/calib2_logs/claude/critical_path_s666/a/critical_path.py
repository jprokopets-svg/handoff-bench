def critical_path(durations: dict, deps: list) -> tuple:
    """
    Compute the critical path in a project network.
    
    Args:
        durations: dict mapping task id -> duration
        deps: list of (a, b) tuples meaning task a must complete before task b
    
    Returns:
        (project_duration, critical_path_list) where:
        - project_duration is the minimum time to complete all tasks
        - critical_path_list is a list of task ids on one longest path
    
    Raises:
        ValueError: if the dependency graph contains a cycle
    """
    
    # Handle empty case
    if not durations:
        return (0.0, [])
    
    # Build adjacency list and in-degree count
    graph = {task: [] for task in durations}
    in_degree = {task: 0 for task in durations}
    
    for a, b in deps:
        if a not in graph:
            graph[a] = []
        if b not in graph:
            graph[b] = []
        graph[a].append(b)
        in_degree[b] = in_degree.get(b, 0) + 1
    
    # Topological sort using Kahn's algorithm to detect cycles
    queue = [task for task in durations if in_degree[task] == 0]
    topo_order = []
    in_degree_copy = in_degree.copy()
    
    while queue:
        node = queue.pop(0)
        topo_order.append(node)
        for neighbor in graph[node]:
            in_degree_copy[neighbor] -= 1
            if in_degree_copy[neighbor] == 0:
                queue.append(neighbor)
    
    # Check for cycle
    if len(topo_order) != len(durations):
        raise ValueError("Dependency graph contains a cycle")
    
    # Compute longest path using dynamic programming
    # dist[task] = longest path distance from any source to this task (not including the task itself)
    dist = {task: 0.0 for task in durations}
    parent = {task: None for task in durations}
    
    for task in topo_order:
        # For each task, update its successors
        for successor in graph[task]:
            new_dist = dist[task] + durations[task]
            if new_dist > dist[successor]:
                dist[successor] = new_dist
                parent[successor] = task
    
    # Find the task with maximum total path length
    # total_length[task] = dist[task] + durations[task]
    max_task = None
    max_length = -1
    
    for task in durations:
        total_length = dist[task] + durations[task]
        if total_length > max_length:
            max_length = total_length
            max_task = task
    
    # Reconstruct the critical path by backtracking
    path = []
    current = max_task
    while current is not None:
        path.append(current)
        current = parent[current]
    
    path.reverse()
    
    return (max_length, path)
