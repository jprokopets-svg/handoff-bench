def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    # Build adjacency list
    graph = [[] for _ in range(num_courses)]
    for course, prereq in prerequisites:
        graph[prereq].append(course)
    
    # Three states: 0 = unvisited, 1 = visiting, 2 = visited
    state = [0] * num_courses
    
    def has_cycle(node: int) -> bool:
        if state[node] == 1:  # Currently visiting - cycle detected
            return True
        if state[node] == 2:  # Already visited - no cycle from here
            return False
        
        state[node] = 1  # Mark as visiting
        
        for neighbor in graph[node]:
            if has_cycle(neighbor):
                return True
        
        state[node] = 2  # Mark as visited
        return False
    
    # Check for cycles starting from each node
    for course in range(num_courses):
        if state[course] == 0:  # Unvisited
            if has_cycle(course):
                return False
    
    return True