from collections import deque

def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    """
    Returns True if all courses can be finished given prerequisites.
    
    Args:
        num_courses: Number of courses to take (labeled 0 to num_courses-1)
        prerequisites: List of [course, prerequisite] pairs
        
    Returns:
        True if all courses can be finished (no cycles), False otherwise
    """
    # Build adjacency list and in-degree array
    graph = [[] for _ in range(num_courses)]
    in_degree = [0] * num_courses
    
    # Create the graph
    for course, prereq in prerequisites:
        graph[prereq].append(course)  # prereq -> course
        in_degree[course] += 1
    
    # Initialize queue with courses having no prerequisites
    queue = deque([i for i in range(num_courses) if in_degree[i] == 0])
    
    # Count of courses we can process
    processed_count = 0
    
    # Process courses in topological order
    while queue:
        course = queue.popleft()
        processed_count += 1
        
        # Reduce in-degree of neighbors
        for neighbor in graph[course]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # If we processed all courses, there's no cycle
    return processed_count == num_courses