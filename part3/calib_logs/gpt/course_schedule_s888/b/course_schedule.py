from collections import deque
from typing import List


def can_finish(num_courses: int, prerequisites: List[List[int]]) -> bool:
    """Return True if it's possible to finish all courses given prerequisites.

    Uses Kahn's algorithm (BFS topological sort). Validates input pairs.
    Raises ValueError for malformed prerequisites or out-of-range indices.
    """
    if not isinstance(num_courses, int) or num_courses < 0:
        raise ValueError("num_courses must be a non-negative integer")

    # quick cases
    if num_courses <= 1:
        return True

    if prerequisites is None:
        prerequisites = []

    # Build adjacency list and indegree array
    adj = [[] for _ in range(num_courses)]
    indeg = [0] * num_courses

    for pair in prerequisites:
        # Validate pair is an iterable with exactly two elements
        if not hasattr(pair, '__iter__'):
            raise ValueError(f"Prerequisite {pair!r} is not iterable of two integers")
        # Convert to list/tuple to check length
        pair_list = list(pair)
        if len(pair_list) != 2:
            raise ValueError(f"Prerequisite {pair!r} does not contain exactly two elements")
        a, b = pair_list
        if not isinstance(a, int) or not isinstance(b, int):
            raise ValueError(f"Prerequisite elements must be integers: {pair!r}")
        if a < 0 or b < 0 or a >= num_courses or b >= num_courses:
            raise ValueError(f"Prerequisite indices out of range for num_courses={num_courses}: {pair!r}")

        # Edge: course a depends on b -> edge b -> a
        adj[b].append(a)
        indeg[a] += 1

    # Initialize queue with nodes of indegree 0
    q = deque([i for i in range(num_courses) if indeg[i] == 0])
    visited = 0

    while q:
        node = q.popleft()
        visited += 1
        for nei in adj[node]:
            indeg[nei] -= 1
            if indeg[nei] == 0:
                q.append(nei)

    return visited == num_courses
