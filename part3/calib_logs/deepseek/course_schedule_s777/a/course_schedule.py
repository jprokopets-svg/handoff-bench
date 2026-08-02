def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    """
    Returns True if all courses can be finished given the number of courses
    and a list of prerequisite pairs [course, prerequisite].
    """
    # Build adjacency list
    graph = [[] for _ in range(num_courses)]
    for course, prereq in prerequisites:
        graph[prereq].append(course)
    
    # States: 0 = unvisited, 1 = visiting (in current DFS path), 2 = visited
    state = [0] * num_courses
    
    def has_cycle(node: int) -> bool:
        if state[node] == 1:
            return True  # Cycle detected
        if state[node] == 2:
            return False  # Already processed
        
        state[node] = 1  # Mark as visiting
        for neighbor in graph[node]:
            if has_cycle(neighbor):
                return True
        state[node] = 2  # Mark as visited
        return False
    
    # Check for cycles starting from each node
    for i in range(num_courses):
        if state[i] == 0:
            if has_cycle(i):
                return False
    return True