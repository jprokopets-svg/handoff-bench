from collections import deque, defaultdict


def can_finish(numCourses, prerequisites):
    """Return True if it's possible to finish all courses (i.e., no cycle) given prerequisites.

    numCourses: int
    prerequisites: list of [course, prerequisite]
    """
    if numCourses <= 1:
        return True

    # Build graph and in-degree counts
    adj = defaultdict(list)
    indegree = [0] * numCourses

    for pair in prerequisites:
        if not pair:
            continue
        # pair is [course, prereq]
        course, prereq = pair
        # add edge prereq -> course
        adj[prereq].append(course)
        indegree[course] += 1

    # Initialize queue with nodes having indegree 0
    q = deque([i for i in range(numCourses) if indegree[i] == 0])
    visited = 0

    while q:
        node = q.popleft()
        visited += 1
        for nei in adj.get(node, []):
            indegree[nei] -= 1
            if indegree[nei] == 0:
                q.append(nei)

    return visited == numCourses


# For manual quick testing
if __name__ == "__main__":
    print(can_finish(2, [[1,0]]))
