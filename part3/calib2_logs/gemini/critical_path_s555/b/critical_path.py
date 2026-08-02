
def critical_path(durations: dict, deps: list) -> tuple:
    if not durations:
        return (0.0, [])

    # Build adjacency list and in-degree map
    adj = {task: [] for task in durations}
    in_degree = {task: 0 for task in durations}
    for u, v in deps:
        adj[u].append(v)
        in_degree[v] += 1

    # Topological sort (Kahn's algorithm)
    q = [task for task in durations if in_degree[task] == 0]
    topological_order = []
    while q:
        u = q.pop(0)
        topological_order.append(u)
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                q.append(v)

    if len(topological_order) != len(durations):
        raise ValueError("Cycle detected in dependency graph")

    # Calculate earliest start times and longest path to each task
    earliest_start_time = {task: 0.0 for task in durations}
    longest_path_to = {task: [task] for task in durations}

    for u in topological_order:
        for v in adj[u]:
            if earliest_start_time[u] + durations[u] > earliest_start_time[v]:
                earliest_start_time[v] = earliest_start_time[u] + durations[u]
                longest_path_to[v] = longest_path_to[u] + [v]

    # Find project duration and critical path
    project_duration = 0.0
    critical_path_tasks = []
    for task in durations:
        finish_time = earliest_start_time[task] + durations[task]
        if finish_time > project_duration:
            project_duration = finish_time
            critical_path_tasks = longest_path_to[task]

    return (project_duration, critical_path_tasks)
