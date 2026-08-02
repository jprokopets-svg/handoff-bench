from collections import deque

def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    """
    Determine if all courses can be completed given prerequisite constraints.
    Uses Kahn's algorithm (topological sort via BFS) to detect cycles.
    
    Args:
        num_courses: Total number of courses (0 to num_courses-1)
        prerequisites: List of [course, prerequisite] pairs
    
    Returns:
        True if all courses can be finished (no cycles), False otherwise
    """
    # Edge case: no courses
    if num_courses == 0:
        return True
    
    # Build adjacency list and in-degree array
    graph = [[] for _ in range(num_courses)]
    in_degree = [0] * num_courses
    
    for course, prerequisite in prerequisites:
        graph[prerequisite].append(course)
        in_degree[course] += 1
    
    # Initialize queue with courses that have no prerequisites
    queue = deque()
    for i in range(num_courses):
        if in_degree[i] == 0:
            queue.append(i)
    
    # Process courses in topological order
    completed = 0
    while queue:
        course = queue.popleft()
        completed += 1
        
        # For each course that depends on the current course
        for next_course in graph[course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)
    
    # If we completed all courses, no cycle exists
    return completed == num_courses
