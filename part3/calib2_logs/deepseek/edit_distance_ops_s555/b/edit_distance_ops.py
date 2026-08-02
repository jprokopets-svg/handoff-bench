def min_edit_ops(a: str, b: str) -> list[tuple]:
    # Handle empty cases
    if a == b:
        return []
    
    m, n = len(a), len(b)
    
    # DP table for Levenshtein distance
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize first row and column
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i-1] == b[j-1]:
                cost = 0
            else:
                cost = 1
            dp[i][j] = min(
                dp[i-1][j] + 1,      # delete
                dp[i][j-1] + 1,      # insert  
                dp[i-1][j-1] + cost  # substitute or match
            )
    
    # Backtrack to find operations
    ops = []
    i, j = m, n
    
    while i > 0 or j > 0:
        if i > 0 and j > 0 and a[i-1] == b[j-1]:
            # Match - no operation needed
            i -= 1
            j -= 1
        else:
            # Check which operation was taken
            if i > 0 and j > 0 and dp[i][j] == dp[i-1][j-1] + 1:
                # Substitute
                ops.append(('sub', i-1, b[j-1]))
                i -= 1
                j -= 1
            elif i > 0 and dp[i][j] == dp[i-1][j] + 1:
                # Delete
                ops.append(('delete', i-1))
                i -= 1
            else:  # j > 0 and dp[i][j] == dp[i][j-1] + 1
                # Insert
                ops.append(('insert', i, b[j-1]))
                j -= 1
    
    # Reverse operations since we backtracked from end to start
    ops.reverse()
    
    # Now we need to adjust indices for sequential application
    # The indices in ops currently refer to positions in the original string 'a'
    # But after each operation, indices shift
    adjusted_ops = []
    current_str = list(a)
    
    for op in ops:
        if op[0] == 'delete':
            # Delete at index op[1] in current string
            adjusted_ops.append(('delete', op[1]))
            del current_str[op[1]]
        elif op[0] == 'insert':
            # Insert at index op[1] in current string
            adjusted_ops.append(('insert', op[1], op[2]))
            current_str.insert(op[1], op[2])
        else:  # 'sub'
            # Substitute at index op[1] in current string
            adjusted_ops.append(('sub', op[1], op[2]))
            current_str[op[1]] = op[2]
    
    return adjusted_ops