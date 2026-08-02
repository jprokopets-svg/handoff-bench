def min_edit_ops(a: str, b: str) -> list[tuple]:
    """
    Return a minimal sequence of edit operations transforming string a into string b.
    Operations: ('delete', i), ('insert', i, c), ('sub', i, c)
    The number of operations equals the Levenshtein distance.
    """
    m, n = len(a), len(b)
    
    # Build DP table for Levenshtein distance
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i-1] == b[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],      # delete from a
                    dp[i][j-1],      # insert into a
                    dp[i-1][j-1]     # substitute
                )
    
    # Backtrack to find operations
    # We'll build operations in reverse order, then reverse at the end
    ops = []
    i, j = m, n
    
    while i > 0 or j > 0:
        if i == 0:
            # Need to insert remaining characters from b
            ops.append(('insert', 0, b[j-1]))
            j -= 1
        elif j == 0:
            # Need to delete remaining characters from a
            ops.append(('delete', 0))
            i -= 1
        elif a[i-1] == b[j-1]:
            # Characters match, no operation needed
            i -= 1
            j -= 1
        else:
            # Characters don't match, find which operation was used
            delete_cost = dp[i-1][j]
            insert_cost = dp[i][j-1]
            sub_cost = dp[i-1][j-1]
            
            if sub_cost <= delete_cost and sub_cost <= insert_cost:
                # Substitute
                ops.append(('sub', i-1, b[j-1]))
                i -= 1
                j -= 1
            elif delete_cost <= insert_cost:
                # Delete
                ops.append(('delete', i-1))
                i -= 1
            else:
                # Insert
                ops.append(('insert', i, b[j-1]))
                j -= 1
    
    # Reverse because we built the operations backwards
    ops.reverse()
    
    # Now adjust indices to account for cumulative changes
    # We need to replay the operations and track index shifts
    adjusted_ops = []
    
    for op in ops:
        if op[0] == 'delete':
            # Delete at original index, but we need to adjust based on prior deletes/inserts
            # Count how many deletes happened before this index
            deletes_before = sum(1 for prev_op in adjusted_ops if prev_op[0] == 'delete' and prev_op[1] < op[1])
            inserts_before = sum(1 for prev_op in adjusted_ops if prev_op[0] == 'insert' and prev_op[1] <= op[1])
            adjusted_index = op[1] - deletes_before + inserts_before
            adjusted_ops.append(('delete', adjusted_index))
        elif op[0] == 'insert':
            # Insert at original index, adjust for prior operations
            deletes_before = sum(1 for prev_op in adjusted_ops if prev_op[0] == 'delete' and prev_op[1] < op[1])
            inserts_before = sum(1 for prev_op in adjusted_ops if prev_op[0] == 'insert' and prev_op[1] < op[1])
            adjusted_index = op[1] - deletes_before + inserts_before
            adjusted_ops.append(('insert', adjusted_index, op[2]))
        else:  # 'sub'
            # Substitute at original index, adjust for prior operations
            deletes_before = sum(1 for prev_op in adjusted_ops if prev_op[0] == 'delete' and prev_op[1] < op[1])
            inserts_before = sum(1 for prev_op in adjusted_ops if prev_op[0] == 'insert' and prev_op[1] <= op[1])
            adjusted_index = op[1] - deletes_before + inserts_before
            adjusted_ops.append(('sub', adjusted_index, op[2]))
    
    return adjusted_ops
