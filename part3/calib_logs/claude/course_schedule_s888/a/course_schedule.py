def can_finish(numCourses, prerequisites):
    """
    Determine if all courses can be finished given prerequisites.
    
    Args:
        numCourses: Number of courses (0 to numCourses-1)
        prerequisites: List of [course, prerequisite] pairs
    
    Returns:
        True if all courses can be finished (no cycles), False otherwise
    """
    # Build adjacency list for the graph
    graph = [[] for _ in range(numCourses)]
    in_degree = [0] * numCourses
    
    for course, prerequisite in prerequisites:
        graph[prerequisite].append(course)
        in_degree[course] += 1
    
    # Kahn's algorithm for topological sort (cycle detection)
    queue = []
    
    # Start with courses that have no prerequisites
    for i in range(numCourses):
        if in_degree[i] == 0:
            queue.append(i)
    
    completed = 0
    
    while queue:
        current = queue.pop(0)
        completed += 1
        
        # For each course that depends on the current course
        for next_course in graph[current]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)
    
    # If we completed all courses, there's no cycle
    return completed == numCourses
