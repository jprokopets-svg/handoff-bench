from collections import deque

def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    """
    Determine if all courses can be completed given prerequisite constraints.
    Uses Kahn's algorithm (topological sort) to detect cycles.
    
    Args:
        num_courses: Total number of courses (0 to num_courses-1)
        prerequisites: List of [course, prerequisite] pairs
        
    Returns:
        True if all courses can be finished (no cycle), False otherwise
    """
    # Build adjacency list and in-degree array
    graph = [[] for _ in range(num_courses)]
    in_degree = [0] * num_courses
    
    # Process prerequisites: course depends on prerequisite
    for course, prerequisite in prerequisites:
        graph[prerequisite].append(course)
        in_degree[course] += 1
    
    # Initialize queue with courses that have no prerequisites
    queue = deque()
    for i in range(num_courses):
        if in_degree[i] == 0:
            queue.append(i)
    
    # Process courses using BFS (Kahn's algorithm)
    completed = 0
    while queue:
        course = queue.popleft()
        completed += 1
        
        # For each course that depends on the current course
        for dependent in graph[course]:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
    
    # If we completed all courses, no cycle exists
    return completed == num_courses
