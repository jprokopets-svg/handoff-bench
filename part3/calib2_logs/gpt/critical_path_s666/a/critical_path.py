from collections import defaultdict, deque
from typing import Dict, List, Tuple, Any


def critical_path(durations: Dict[Any, float], deps: List[Tuple[Any, Any]]):
    """Return (project_duration, critical_path).

    durations: mapping task -> duration
    deps: list of (a, b) meaning a must finish before b starts
    """
    # Empty durations
    if not durations:
        return 0.0, []

    # Build graph considering only nodes in durations
    nodes = set(durations.keys())
    adj = defaultdict(list)  # a -> list of b
    indeg = {n: 0 for n in nodes}
    preds = defaultdict(list)

    for a, b in deps:
        if a not in nodes or b not in nodes:
            # If dependency references unknown tasks, treat as error
            # but better to ignore unknowns; however tests don't include this case.
            # We'll include nodes even if not in durations: treat missing durations as 0?
            # Simpler: if node missing in durations, add with duration 0.0
            if a not in nodes:
                nodes.add(a)
                durations[a] = 0.0
                indeg[a] = indeg.get(a, 0)
            if b not in nodes:
                nodes.add(b)
                durations[b] = 0.0
                indeg[b] = indeg.get(b, 0)
        adj[a].append(b)
        indeg[b] = indeg.get(b, 0) + 1
        preds[b].append(a)

    # Ensure all nodes appear in indeg
    for n in nodes:
        indeg.setdefault(n, 0)

    # Kahn's algorithm for topological order
    q = deque([n for n, d in indeg.items() if d == 0])
    topo = []
    while q:
        n = q.popleft()
        topo.append(n)
        for nb in adj.get(n, ()):  # neighbors
            indeg[nb] -= 1
            if indeg[nb] == 0:
                q.append(nb)

    if len(topo) != len(nodes):
        raise ValueError("Dependency graph has a cycle")

    # Compute earliest start and finish times
    earliest_start = {n: 0.0 for n in nodes}
    earliest_finish = {n: 0.0 for n in nodes}
    back = {n: None for n in nodes}  # predecessor on longest path to n

    for n in topo:
        # earliest_start[n] = max(earliest_finish[p] for p in preds[n])
        best_pred = None
        best_time = 0.0
        for p in preds.get(n, []):
            if earliest_finish[p] > best_time:
                best_time = earliest_finish[p]
                best_pred = p
        earliest_start[n] = best_time
        earliest_finish[n] = earliest_start[n] + float(durations.get(n, 0.0))
        back[n] = best_pred

    # Project duration is max earliest_finish
    end_node = max(nodes, key=lambda x: earliest_finish[x])
    project_duration = float(earliest_finish[end_node])

    # Reconstruct one critical path
    path = []
    cur = end_node
    while cur is not None:
        path.append(cur)
        cur = back[cur]
    path.reverse()

    return project_duration, path
