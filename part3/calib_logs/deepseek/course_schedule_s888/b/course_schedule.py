def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    # Build adjacency list and in-degree array
    graph = [[] for _ in range(num_courses)]
    in_degree = [0] * num_courses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1
    
    # Kahn's algorithm for topological sort
    # Find all nodes with in-degree 0
    queue = []
    for i in range(num_courses):
        if in_degree[i] == 0:
            queue.append(i)
    
    count_visited = 0
    
    while queue:
        node = queue.pop(0)
        count_visited += 1
        
        # Reduce in-degree of neighbors
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # If we visited all nodes, there's no cycle
    return count_visited == num_courses