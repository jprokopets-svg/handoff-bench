def can_finish(num_courses, prerequisites):
    """
    Determine if all courses can be finished given prerequisites.
    
    Args:
        num_courses: Number of courses (0 to num_courses-1)
        prerequisites: List of [course, prerequisite] pairs
        
    Returns:
        True if all courses can be finished (no cycles), False otherwise
    """
    # Build adjacency list for the graph
    graph = [[] for _ in range(num_courses)]
    in_degree = [0] * num_courses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1
    
    # Topological sort using Kahn's algorithm (BFS)
    queue = []
    
    # Start with courses that have no prerequisites
    for i in range(num_courses):
        if in_degree[i] == 0:
            queue.append(i)
    
    completed = 0
    
    while queue:
        course = queue.pop(0)
        completed += 1
        
        # For each course that depends on the current course
        for next_course in graph[course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)
    
    # If we completed all courses, there's no cycle
    return completed == num_courses
