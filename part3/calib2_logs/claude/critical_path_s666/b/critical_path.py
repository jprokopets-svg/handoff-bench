def critical_path(durations: dict, deps: list) -> tuple:
    """
    Compute the critical path in a project network.
    
    Args:
        durations: dict mapping task id -> duration
        deps: list of (a, b) tuples meaning task a must complete before task b
    
    Returns:
        (project_duration, critical_path_list)
        - project_duration: minimum time to complete all tasks
        - critical_path_list: list of task ids on the longest path
    
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
        if a not in graph:
            graph[a] = []
        if b not in graph:
            graph[b] = []
        graph[a].append(b)
        in_degree[b] = in_degree.get(b, 0) + 1
    
    # Kahn's algorithm for topological sort + cycle detection
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
    
    # Dynamic programming: compute longest path ending at each node
    longest_path_length = {task: durations[task] for task in durations}
    parent = {task: None for task in durations}
    
    for node in topo_order:
        for neighbor in graph[node]:
            if longest_path_length[node] + durations[neighbor] > longest_path_length[neighbor]:
                longest_path_length[neighbor] = longest_path_length[node] + durations[neighbor]
                parent[neighbor] = node
    
    # Find the task with maximum longest path length
    max_duration = max(longest_path_length.values())
    end_task = max(longest_path_length, key=longest_path_length.get)
    
    # Reconstruct the critical path by backtracking through parents
    path = []
    current = end_task
    while current is not None:
        path.append(current)
        current = parent[current]
    
    path.reverse()
    
    return (max_duration, path)
