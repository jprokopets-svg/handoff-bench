from typing import List


def can_finish(numCourses: int, prerequisites: List[List[int]]) -> bool:
    """Return True if it's possible to finish all courses given prerequisites.

    Use DFS to detect cycles in directed graph. prerequisites are pairs [a,b]
    meaning to take course a you must first take course b (edge b -> a).
    """
    # Build adjacency list
    adj = [[] for _ in range(numCourses)]
    for a, b in prerequisites:
        if 0 <= b < numCourses and 0 <= a < numCourses:
            adj[b].append(a)

    # 0 = unvisited, 1 = visiting, 2 = visited
    state = [0] * numCourses

    def dfs(u: int) -> bool:
        if state[u] == 1:
            return False  # found cycle
        if state[u] == 2:
            return True
        state[u] = 1
        for v in adj[u]:
            if not dfs(v):
                return False
        state[u] = 2
        return True

    for i in range(numCourses):
        if state[i] == 0:
            if not dfs(i):
                return False
    return True
