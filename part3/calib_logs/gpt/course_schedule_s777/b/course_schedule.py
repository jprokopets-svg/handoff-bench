from collections import deque


def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    """
    Determine if all courses can be finished given prerequisites.
    Uses Kahn's algorithm (BFS/topological sort) to detect cycles without recursion.
    Invalid prerequisite pairs (indices out of range) are ignored.
    """
    if num_courses <= 0:
        return True

    indegree = [0] * num_courses
    adj = [[] for _ in range(num_courses)]

    for pair in prerequisites:
        if not pair or len(pair) < 2:
            continue
        course, prereq = pair[0], pair[1]
        if 0 <= course < num_courses and 0 <= prereq < num_courses:
            adj[prereq].append(course)
            indegree[course] += 1
        else:
            # ignore invalid indices
            continue

    q = deque([i for i in range(num_courses) if indegree[i] == 0])
    visited = 0

    while q:
        node = q.popleft()
        visited += 1
        for nei in adj[node]:
            indegree[nei] -= 1
            if indegree[nei] == 0:
                q.append(nei)

    return visited == num_courses
