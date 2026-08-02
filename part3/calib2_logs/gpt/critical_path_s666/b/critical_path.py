from collections import deque


def critical_path(durations: dict, deps: list) -> tuple:
    # Return (project_duration, critical_path)
    # Copy durations to avoid mutating caller's dict
    if not durations:
        # If durations is empty, return (0.0, []) per spec
        return 0.0, []

    local_durations = dict(durations)

    # Collect all nodes, include ones appearing in deps
    for a, b in deps:
        if a not in local_durations:
            local_durations[a] = 0.0
        if b not in local_durations:
            local_durations[b] = 0.0

    nodes = list(local_durations.keys())

    # Build adjacency and indegree
    adj = {n: [] for n in nodes}
    indegree = {n: 0 for n in nodes}
    for a, b in deps:
        adj[a].append(b)
        indegree[b] += 1

    # Kahn's algorithm for topological sort
    q = deque([n for n in nodes if indegree[n] == 0])
    topo = []
    while q:
        n = q.popleft()
        topo.append(n)
        for m in adj[n]:
            indegree[m] -= 1
            if indegree[m] == 0:
                q.append(m)

    if len(topo) != len(nodes):
        raise ValueError("Dependency graph has a cycle")

    # Compute earliest start times (longest path in DAG)
    est = {n: 0.0 for n in nodes}
    for n in topo:
        finish = est[n] + float(local_durations[n])
        for m in adj[n]:
            if est[m] < finish:
                est[m] = finish

    # Project duration = max finish time
    finishes = {n: est[n] + float(local_durations[n]) for n in nodes}
    project_duration = max(finishes.values()) if finishes else 0.0

    # Find a sink node achieving project duration
    # Use first encountered in nodes order
    target = None
    for n in nodes:
        if abs(finishes[n] - project_duration) < 1e-12:
            target = n
            break

    if target is None:
        return float(project_duration), []

    # Build predecessors mapping for backtracking
    preds = {n: [] for n in nodes}
    for a, b in deps:
        preds[b].append(a)

    # Reconstruct one critical path by moving to any predecessor p
    # such that est[p] + dur[p] == est[cur]
    path_rev = [target]
    cur = target
    while True:
        found = False
        for p in preds[cur]:
            if abs((est[p] + float(local_durations[p])) - est[cur]) < 1e-12:
                path_rev.append(p)
                cur = p
                found = True
                break
        if not found:
            break

    path = list(reversed(path_rev))
    return float(project_duration), path
