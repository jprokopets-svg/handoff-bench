def min_edit_ops(a: str, b: str) -> list:
    """Return a minimal sequence of edit operations transforming a into b.
    
    Operations are:
    - ('delete', i): delete character at index i
    - ('insert', i, c): insert character c at index i  
    - ('sub', i, c): replace character at index i with c
    
    Indices refer to the state after all prior operations.
    Number of operations equals Levenshtein distance (uniform cost 1).
    """
    if a == b:
        return []
    
    m, n = len(a), len(b)
    # DP table for distances
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
                dp[i-1][j] + 1,      # delete from a
                dp[i][j-1] + 1,      # insert into a
                dp[i-1][j-1] + cost  # substitute or match
            )
    
    # Backtrack to find operations (in reverse order)
    ops_rev = []
    i, j = m, n
    
    while i > 0 or j > 0:
        if i > 0 and j > 0 and a[i-1] == b[j-1]:
            # Match, no operation needed
            i -= 1
            j -= 1
        else:
            # Check which operation was used
            if i > 0 and j > 0 and dp[i][j] == dp[i-1][j-1] + 1:
                # Substitution
                # Character a[i-1] becomes b[j-1]
                # In the current string during forward execution,
                # position i-1 corresponds to the character we're processing
                ops_rev.append(('sub', i-1, b[j-1]))
                i -= 1
                j -= 1
            elif i > 0 and dp[i][j] == dp[i-1][j] + 1:
                # Deletion of a[i-1]
                ops_rev.append(('delete', i-1))
                i -= 1
            else:  # j > 0 and dp[i][j] == dp[i][j-1] + 1
                # Insertion of b[j-1]
                # Insert at position i (after i characters from original processed)
                ops_rev.append(('insert', i, b[j-1]))
                j -= 1
    
    # Reverse to get forward order
    ops_rev.reverse()
    
    # Now we need to adjust indices because operations affect subsequent indices
    # We'll simulate the operations to compute correct indices
    current = list(a)
    result_ops = []
    
    for op in ops_rev:
        if op[0] == 'delete':
            result_ops.append(('delete', op[1]))
            del current[op[1]]
        elif op[0] == 'insert':
            result_ops.append(('insert', op[1], op[2]))
            current.insert(op[1], op[2])
        else:  # 'sub'
            result_ops.append(('sub', op[1], op[2]))
            current[op[1]] = op[2]
    
    return result_ops