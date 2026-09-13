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
    # We'll build the operations directly with correct indices
    # by simulating the transformation as we go
    ops = []
    i, j = m, n
    
    # We'll simulate the string transformation in reverse
    # Starting from the end of the transformation
    current_pos = m  # position in the current string (starting from end)
    
    while i > 0 or j > 0:
        if i > 0 and j > 0 and a[i-1] == b[j-1]:
            # Match, no operation needed
            i -= 1
            j -= 1
            current_pos -= 1
        else:
            # Check which operation was used
            if i > 0 and j > 0 and dp[i][j] == dp[i-1][j-1] + 1:
                # Substitution at position current_pos-1
                ops.append(('sub', current_pos-1, b[j-1]))
                i -= 1
                j -= 1
                current_pos -= 1
            elif i > 0 and dp[i][j] == dp[i-1][j] + 1:
                # Deletion at position current_pos-1
                ops.append(('delete', current_pos-1))
                i -= 1
                current_pos -= 1
            else:  # j > 0 and dp[i][j] == dp[i][j-1] + 1
                # Insertion at position current_pos
                ops.append(('insert', current_pos, b[j-1]))
                j -= 1
                # current_pos doesn't change for insertion (we're inserting before current_pos)
    
    # Reverse to get forward order
    ops.reverse()
    return ops