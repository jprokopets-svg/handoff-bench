def min_edit_ops(a: str, b: str) -> list[tuple]:
    """
    Return a minimal sequence of edit operations transforming string a into string b.
    Operations: ('delete', i), ('insert', i, c), ('sub', i, c)
    The number of operations equals the Levenshtein distance.
    """
    if a == b:
        return []
    
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
                    dp[i-1][j],      # delete
                    dp[i][j-1],      # insert
                    dp[i-1][j-1]     # substitute
                )
    
    # Backtrack to find operations (in reverse order)
    ops_reverse = []
    i, j = m, n
    
    while i > 0 or j > 0:
        if i == 0:
            # Need to insert remaining characters from b
            ops_reverse.append(('insert', j-1, b[j-1]))
            j -= 1
        elif j == 0:
            # Need to delete remaining characters from a
            ops_reverse.append(('delete', i-1))
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
                ops_reverse.append(('sub', i-1, b[j-1]))
                i -= 1
                j -= 1
            elif delete_cost <= insert_cost:
                # Delete
                ops_reverse.append(('delete', i-1))
                i -= 1
            else:
                # Insert
                ops_reverse.append(('insert', i, b[j-1]))
                j -= 1
    
    # Reverse to get forward operations
    ops_reverse.reverse()
    
    # Now we need to adjust indices for forward application
    # Apply operations and track index adjustments
    ops = []
    current_str = list(a)
    
    for op in ops_reverse:
        if op[0] == 'delete':
            ops.append(op)
            del current_str[op[1]]
        elif op[0] == 'insert':
            ops.append(op)
            current_str.insert(op[1], op[2])
        else:  # 'sub'
            ops.append(op)
            current_str[op[1]] = op[2]
    
    return ops
