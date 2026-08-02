from collections import defaultdict, deque


def critical_path(durations, deps):
    """
    durations: dict task -> duration (number)
    deps: list of (a,b) pairs meaning a must finish before b starts

    Returns (project_duration, critical_path_list)
    Raises ValueError on cycles. If durations empty, return (0.0, []).
    """
    # If no durations, nothing to do
    if not durations:
        return 0.0, []

    # Collect nodes: include any nodes mentioned in deps as well
    nodes = set(durations.keys())
    for a, b in deps:
        nodes.add(a)
        nodes.add(b)

    # Use durations.get(node, 0.0) to allow nodes mentioned in deps but not in durations
    dur = {n: float(durations.get(n, 0.0)) for n in nodes}

    # Build graph
    adj = defaultdict(list)
    preds = defaultdict(list)
    indeg = {n: 0 for n in nodes}
    for a, b in deps:
        adj[a].append(b)
        preds[b].append(a)
        indeg[b] = indeg.get(b, 0) + 1
        # ensure indeg entry exists for a
        if a not in indeg:
            indeg[a] = indeg.get(a, 0)

    # Kahn's algorithm for topological sort
    q = deque([n for n in nodes if indeg.get(n, 0) == 0])
    topo = []
    while q:
        n = q.popleft()
        topo.append(n)
        for nb in adj.get(n, []):
            indeg[nb] -= 1
            if indeg[nb] == 0:
                q.append(nb)

    if len(topo) != len(nodes):
        raise ValueError("Cycle detected in dependencies")

    # Compute earliest finish times and predecessor for longest path
    earliest_finish = {}
    prev = {}
    for n in topo:
        # If no predecessors, start at 0
        best_pred = None
        best_pred_finish = 0.0
        for p in preds.get(n, []):
            pf = earliest_finish.get(p, 0.0)
            if pf > best_pred_finish:
                best_pred_finish = pf
                best_pred = p
        earliest_finish[n] = best_pred_finish + dur.get(n, 0.0)
        prev[n] = best_pred

    # Project duration is max earliest_finish
    end_node = max(earliest_finish.keys(), key=lambda x: earliest_finish[x])
    project_duration = float(earliest_finish[end_node])

    # Reconstruct path from end_node backwards
    path = []
    cur = end_node
    while cur is not None:
        path.append(cur)
        cur = prev.get(cur)
    path.reverse()

    return project_duration, path
