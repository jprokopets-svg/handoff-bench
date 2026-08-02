from collections import defaultdict, deque

def critical_path(durations, dependencies):
    """
    Given task durations (mapping task id -> duration) and dependency pairs (a, b)
    meaning task a must complete before task b can start, return (project_duration, critical_path).
    
    project_duration is the minimum time to finish ALL tasks assuming unlimited parallel execution.
    critical_path is a list of task ids on ONE longest path from any source to any sink.
    
    If the dependency graph contains a cycle, raise ValueError.
    If durations is empty, return (0.0, []).
    """
    if not durations:
        return 0.0, []
    
    # Build adjacency list and indegree
    graph = defaultdict(list)
    indegree = defaultdict(int)
    for a, b in dependencies:
        graph[a].append(b)
        indegree[b] += 1
        # Ensure all nodes are in indegree dict
        if a not in indegree:
            indegree[a] = 0
    
    # Add nodes with no dependencies
    for task in durations:
        if task not in indegree:
            indegree[task] = 0
    
    # Topological sort with cycle detection
    zero_indegree = deque([task for task in indegree if indegree[task] == 0])
    topo_order = []
    
    while zero_indegree:
        task = zero_indegree.popleft()
        topo_order.append(task)
        for neighbor in graph[task]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                zero_indegree.append(neighbor)
    
    # Check for cycle
    if len(topo_order) != len(indegree):
        raise ValueError("Graph contains a cycle")
    
    # Forward pass: compute earliest start times
    earliest_start = {task: 0.0 for task in durations}
    for task in topo_order:
        for neighbor in graph[task]:
            earliest_start[neighbor] = max(
                earliest_start[neighbor],
                earliest_start[task] + durations[task]
            )
    
    # Project duration is max of earliest finish times
    project_duration = 0.0
    for task in durations:
        finish_time = earliest_start[task] + durations[task]
        if finish_time > project_duration:
            project_duration = finish_time
    
    # Backward pass: compute latest start times
    latest_start = {task: float('inf') for task in durations}
    # Initialize latest start for tasks with no dependents (sinks)
    for task in durations:
        if not graph[task]:  # No outgoing edges
            latest_start[task] = project_duration - durations[task]
    
    # Process in reverse topological order
    for task in reversed(topo_order):
        # Update predecessors
        for neighbor in graph[task]:
            latest_start[task] = min(
                latest_start[task],
                latest_start[neighbor] - durations[task]
            )
    
    # Identify critical tasks: earliest_start == latest_start
    critical_tasks = set()
    for task in durations:
        if abs(earliest_start[task] - latest_start[task]) < 1e-9:
            critical_tasks.add(task)
    
    # Build one critical path from source to sink
    # Find a source task (no incoming edges) that is critical
    sources = [task for task in durations if task not in {b for a, b in dependencies}]
    critical_source = None
    for source in sources:
        if source in critical_tasks:
            critical_source = source
            break
    
    # If no critical source found (shouldn't happen), pick any critical task
    if critical_source is None and critical_tasks:
        critical_source = next(iter(critical_tasks))
    
    # Reconstruct path from source following critical edges
    path = []
    current = critical_source
    while current is not None:
        path.append(current)
        # Find a critical successor
        next_task = None
        for neighbor in graph[current]:
            if neighbor in critical_tasks:
                # Check if edge is critical: earliest_start[current] + durations[current] == earliest_start[neighbor]
                if abs(earliest_start[current] + durations[current] - earliest_start[neighbor]) < 1e-9:
                    next_task = neighbor
                    break
        
        current = next_task
    
    return project_duration, path