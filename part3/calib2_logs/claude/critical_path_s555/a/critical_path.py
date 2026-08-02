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
        graph[a].append(b)
        in_degree[b] += 1
    
    # Topological sort with cycle detection using Kahn's algorithm
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
    # longest[task] = (max_duration_ending_at_task, predecessor_on_critical_path)
    # This includes the task's own duration
    longest = {task: (durations[task], None) for task in durations}
    
    for task in topo_order:
        # Update all successors
        for successor in graph[task]:
            new_duration = longest[task][0] + durations[successor]
            if new_duration > longest[successor][0]:
                longest[successor] = (new_duration, task)
    
    # Find the sink node(s) with maximum duration
    max_duration = 0.0
    sink_task = None
    for task in durations:
        if longest[task][0] > max_duration:
            max_duration = longest[task][0]
            sink_task = task
    
    # Reconstruct the critical path by backtracking
    path = []
    current = sink_task
    while current is not None:
        path.append(current)
        current = longest[current][1]
    
    path.reverse()
    
    return (max_duration, path)
