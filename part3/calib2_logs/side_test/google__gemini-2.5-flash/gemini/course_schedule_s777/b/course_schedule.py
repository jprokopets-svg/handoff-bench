from collections import deque

def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    adj = [[] for _ in range(num_courses)]
    in_degree = [0] * num_courses

    for course, prereq in prerequisites:
        adj[prereq].append(course)
        in_degree[course] += 1

    queue = deque([i for i in range(num_courses) if in_degree[i] == 0])
    count = 0

    while queue:
        prereq = queue.popleft()
        count += 1

        for course in adj[prereq]:
            in_degree[course] -= 1
            if in_degree[course] == 0:
                queue.append(course)

    return count == num_courses
