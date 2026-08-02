import collections

def critical_path(durations, deps):
    if not durations:
        return 0.0, []

    # Build adjacency list and in-degree map
    adj = collections.defaultdict(list)
    in_degree = collections.defaultdict(int)
    for u, v in deps:
        adj[u].append(v)
        in_degree[v] += 1
        # Ensure all tasks are in in_degree map, even if they have no dependencies
        in_degree[u] 

    # Initialize all tasks with 0 in-degree as sources
    sources = collections.deque([task for task in durations if in_degree[task] == 0])

    # Calculate earliest start times and longest path to each task
    earliest_start_time = collections.defaultdict(float)
    longest_path_to_task = collections.defaultdict(list)

    for task in durations:
        earliest_start_time[task] = 0.0
        longest_path_to_task[task] = [task]

    while sources:
        u = sources.popleft()

        for v in adj[u]:
            new_start_time = earliest_start_time[u] + durations[u]
            if new_start_time > earliest_start_time[v]:
                earliest_start_time[v] = new_start_time
                longest_path_to_task[v] = longest_path_to_task[u] + [v]
            
            in_degree[v] -= 1
            if in_degree[v] == 0:
                sources.append(v)

    # Check for cycles
    if any(in_degree[task] != 0 for task in durations):
        raise ValueError("Dependency graph contains a cycle")

    # Find the project duration and critical path
    project_duration = 0.0
    critical_path_tasks = []

    for task in durations:
        finish_time = earliest_start_time[task] + durations[task]
        if finish_time > project_duration:
            project_duration = finish_time
            critical_path_tasks = longest_path_to_task[task]

    return project_duration, critical_path_tasks
