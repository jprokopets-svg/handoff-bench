from collections import defaultdict, deque
import heapq


def critical_path(durations: dict, deps: list) -> tuple:
    # If durations is empty, return as specified
    if not durations:
        return (0.0, [])

    # Collect all nodes from durations and deps
    nodes = set(durations.keys())
    for a, b in deps:
        nodes.add(a)
        nodes.add(b)

    # Ensure duration default for nodes not in durations
    dur = {n: float(durations.get(n, 0.0)) for n in nodes}

    # Build graph: adjacency list and predecessors
    adj = defaultdict(list)
    preds = defaultdict(list)
    indeg = {n: 0 for n in nodes}
    for a, b in deps:
        adj[a].append(b)
        preds[b].append(a)
        indeg[b] = indeg.get(b, 0) + 1
        # ensure a in indeg (may have been inserted from durations)
        if a not in indeg:
            indeg[a] = indeg.get(a, 0)

    # Kahn's algorithm for topo sort with deterministic ordering
    # Use a heap with string-key tie-break to be deterministic across runs
    heap = []
    for n in nodes:
        if indeg.get(n, 0) == 0:
            heapq.heappush(heap, (str(n), n))

    topo = []
    while heap:
        _, n = heapq.heappop(heap)
        topo.append(n)
        for m in adj.get(n, ()):  # neighbors
            indeg[m] -= 1
            if indeg[m] == 0:
                heapq.heappush(heap, (str(m), m))

    if len(topo) != len(nodes):
        raise ValueError("Cycle detected in dependencies")

    # Compute earliest finish times: for each node, dur + max(earliest_finish of preds)
    ef = {n: 0.0 for n in nodes}
    for n in topo:
        if not preds[n]:
            ef[n] = dur[n]
        else:
            # choose max over predecessors
            max_pred = max((ef[p] for p in preds[n]), default=0.0)
            ef[n] = dur[n] + max_pred

    # Project duration is max ef
    project_duration = max(ef.values()) if ef else 0.0

    # Find one node that attains project_duration (deterministically pick smallest str key)
    candidates = [n for n, v in ef.items() if abs(v - project_duration) < 1e-12]
    if not candidates:
        return (float(project_duration), [])
    # pick deterministic candidate
    end = sorted(candidates, key=lambda x: str(x))[0]

    # Reconstruct one critical path by backtracking: at each step pick predecessor
    # that satisfies ef[cur] == dur[cur] + ef[pred]. If multiple, pick pred with largest ef,
    # tie-break deterministically by str(pred).
    path = []
    cur = end
    while True:
        path.append(cur)
        if not preds[cur]:
            break
        # select predecessors satisfying the equality
        valid_preds = [p for p in preds[cur] if abs(ef[cur] - (dur[cur] + ef[p])) < 1e-12]
        if not valid_preds:
            # should not happen, but break defensively
            break
        # choose the pred with maximum ef, tie-break by str
        valid_preds.sort(key=lambda x: ( -ef[x], str(x) ))
        cur = valid_preds[0]
    path.reverse()
    return (float(project_duration), path)
