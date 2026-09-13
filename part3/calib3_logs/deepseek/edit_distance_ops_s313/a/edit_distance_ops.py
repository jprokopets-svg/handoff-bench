def min_edit_ops(a: str, b: str) -> list[tuple]:
    """Return a minimal sequence of edit operations transforming a into b.
    
    Operations are:
    - ('delete', i): delete character at index i
    - ('insert', i, c): insert character c at index i
    - ('sub', i, c): replace character at index i with c
    
    Indices refer to the current string state after all prior operations.
    Number of operations equals the Levenshtein distance.
    """
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
            if a[i - 1] == b[j - 1]:
                cost = 0
            else:
                cost = 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,      # delete
                dp[i][j - 1] + 1,      # insert  
                dp[i - 1][j - 1] + cost  # substitute or match
            )
    
    # Backtrack to find operations
    ops = []
    i, j = m, n
    
    while i > 0 or j > 0:
        if i > 0 and j > 0 and a[i - 1] == b[j - 1]:
            # Match - no operation needed
            i -= 1
            j -= 1
        else:
            # Check which operation was used
            if i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
                # Substitution
                # Need to find the correct index in the current string
                # The index is the position in the original string that corresponds
                # to the current position after all previous operations
                ops.append(('sub', i - 1, b[j - 1]))
                i -= 1
                j -= 1
            elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
                # Deletion
                ops.append(('delete', i - 1))
                i -= 1
            else:  # j > 0 and dp[i][j] == dp[i][j - 1] + 1
                # Insertion
                # Insert at position i (after the current character)
                ops.append(('insert', i, b[j - 1]))
                j -= 1
    
    # Reverse operations since we backtracked from end to start
    ops.reverse()
    return ops