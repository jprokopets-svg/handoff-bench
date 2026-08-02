def min_edit_ops(a: str, b: str) -> list[tuple]:
    """Return a minimal sequence of edit operations transforming a into b."""
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
            # Find which operation was used
            if i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
                # Substitution
                # The index for substitution is i-1 in the current string
                # We need to convert this to an index in the state after previous operations
                # Since we're building operations backwards, we need to track how indices shift
                ops.append(('sub', i - 1, b[j - 1]))
                i -= 1
                j -= 1
            elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
                # Deletion
                # Delete at index i-1 in current string
                ops.append(('delete', i - 1))
                i -= 1
            else:  # j > 0 and dp[i][j] == dp[i][j - 1] + 1
                # Insertion
                # Insert at index i in current string (after position i-1)
                ops.append(('insert', i, b[j - 1]))
                j -= 1
    
    # Reverse operations since we built them backwards
    ops.reverse()
    
    # Now we need to adjust indices to account for operations being applied sequentially
    # When we apply operations forward, indices shift due to insertions and deletions
    # We need to convert indices from "original string a" perspective to "current state" perspective
    
    # Track how indices shift as we apply operations
    adjusted_ops = []
    shift = 0  # Positive shift means indices increased due to insertions before them
    
    for op in ops:
        if op[0] == 'delete':
            # Delete at index op[1] in current string
            # Adjust index: original index - deletions before it + insertions before it
            adjusted_idx = op[1] + shift
            adjusted_ops.append(('delete', adjusted_idx))
            # After deletion, indices after this position shift left by 1
            shift -= 1
        elif op[0] == 'insert':
            # Insert at index op[1] in current string
            adjusted_idx = op[1] + shift
            adjusted_ops.append(('insert', adjusted_idx, op[2]))
            # After insertion, indices after this position shift right by 1
            shift += 1
        else:  # 'sub'
            # Substitute at index op[1] in current string
            adjusted_idx = op[1] + shift
            adjusted_ops.append(('sub', adjusted_idx, op[2]))
            # Substitution doesn't change indices
    
    return adjusted_ops