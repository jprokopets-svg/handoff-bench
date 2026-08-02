from collections import deque

def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    """
    Determines if a valid course schedule is possible.

    This function uses Kahn's algorithm for topological sorting to detect cycles
    in the course dependency graph.

    Args:
        num_courses: The total number of courses.
        prerequisites: A list of prerequisite pairs, where [course, prerequisite]
                       means you must take 'prerequisite' before 'course'.

    Returns:
        True if all courses can be finished, False otherwise (if a cycle exists).
    """
    # 1. Initialize graph and in-degrees
    graph = [[] for _ in range(num_courses)]
    in_degree = [0] * num_courses

    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1

    # 2. Initialize the queue with courses having an in-degree of 0
    queue = deque([i for i in range(num_courses) if in_degree[i] == 0])

    # 3. Process the queue
    courses_taken = 0
    while queue:
        course = queue.popleft()
        courses_taken += 1

        for neighbor in graph[course]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # 4. Check if all courses were taken
    return courses_taken == num_courses
