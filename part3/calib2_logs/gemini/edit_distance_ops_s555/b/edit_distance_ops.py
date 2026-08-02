
def min_edit_ops(a: str, b: str) -> list[tuple]:
    n = len(a)
    m = len(b)

    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j],      # Deletion
                                   dp[i][j - 1],      # Insertion
                                   dp[i - 1][j - 1])  # Substitution

    # Backtrack to find the operations
    operations = []
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and a[i - 1] == b[j - 1]:
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            operations.append(('sub', i - 1, b[j - 1]))
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            operations.append(('delete', i - 1))
            i -= 1
        elif j > 0 and dp[i][j] == dp[i][j - 1] + 1:
            operations.append(('insert', i, b[j - 1]))
            j -= 1
    
    operations.reverse()

    # Adjust indices for sequential operations
    final_operations = []
    current_offset = 0
    for op in operations:
        op_type = op[0]
        if op_type == 'delete':
            original_index = op[1]
            final_operations.append(('delete', original_index + current_offset))
            current_offset -= 1
        elif op_type == 'insert':
            original_index = op[1]
            char_to_insert = op[2]
            final_operations.append(('insert', original_index + current_offset, char_to_insert))
            current_offset += 1
        elif op_type == 'sub':
            original_index = op[1]
            char_to_sub = op[2]
            final_operations.append(('sub', original_index + current_offset, char_to_sub))
    
    return final_operations
