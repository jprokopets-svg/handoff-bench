def min_edit_ops(a: str, b: str):
    """Return a minimal sequence of edit operations transforming a into b."""
    if a == b:
        return []
    
    n, m = len(a), len(b)
    # dp[i][j] = distance between a[:i] and b[:j]
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j
    
    # parent for backtracking: 0=sub/equal, 1=delete, 2=insert
    parent = [[-1] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        parent[i][0] = 1  # delete
    for j in range(1, m + 1):
        parent[0][j] = 2  # insert
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if a[i-1] == b[j-1] else 1
            sub = dp[i-1][j-1] + cost
            delete = dp[i-1][j] + 1
            insert = dp[i][j-1] + 1
            
            if sub <= delete and sub <= insert:
                dp[i][j] = sub
                parent[i][j] = 0  # sub or equal
            elif delete <= insert:
                dp[i][j] = delete
                parent[i][j] = 1  # delete
            else:
                dp[i][j] = insert
                parent[i][j] = 2  # insert
    
    # backtrack to build operations
    ops = []
    i, j = n, m
    while i > 0 or j > 0:
        if parent[i][j] == 0:
            # substitution or match
            if a[i-1] != b[j-1]:
                # need substitution
                # index in current string after applying previous ops?
                # We'll compute index later by simulating forward
                ops.append(('sub', i-1, b[j-1]))
            i -= 1
            j -= 1
        elif parent[i][j] == 1:
            # delete a[i-1]
            ops.append(('delete', i-1))
            i -= 1
        else:  # parent[i][j] == 2
            # insert b[j-1] at position i (after a[:i])
            ops.append(('insert', i, b[j-1]))
            j -= 1
    
    # ops are built backwards, reverse
    ops.reverse()
    
    # Now we need to adjust indices because operations are applied sequentially.
    # We'll simulate forward and adjust indices.
    # Better: compute operations directly with forward indices.
    # Let's recompute with forward approach.
    # Actually, we can compute operations in forward direction by walking dp forward.
    # But easier: we have ops with indices relative to original a.
    # We need to convert to sequential indices.
    # We'll simulate the operations on a copy and adjust indices.
    # However, we can compute operations directly with correct indices by
    # tracking current position in a and b.
    
    # Let's implement forward reconstruction.
    # We'll walk through dp from (0,0) to (n,m) building ops.
    # At each step choose optimal operation.
    # We'll keep current index in a (i) and b (j).
    ops = []
    i, j = 0, 0
    while i < n or j < m:
        if i < n and j < m and a[i] == b[j]:
            # match, no operation
            i += 1
            j += 1
            continue
        # check which operation is optimal
        # we need dp values at (i,j) relative to full dp which uses lengths.
        # Actually we have dp table computed with indices 0..n, 0..m.
        # dp[i][j] corresponds to distance between a[i:] and b[j:]? Wait dp[i][j] is prefix.
        # Our dp[i][j] is distance between a[:i] and b[:j].
        # So we need to look at dp[i+1][j+1] etc.
        # Let's use the dp table we already have.
        # Current state corresponds to dp[i][j]? Actually dp[i][j] is distance between prefixes of length i and j.
        # We are at position i in a and j in b (already processed i chars of a and j chars of b).
        # The remaining substrings are a[i:] and b[j:].
        # The distance for remaining is dp[n][m] - dp[i][j]? Not exactly.
        # Better to recompute with forward DP from (i,j) to (n,m).
        # But we can use the dp table to decide locally.
        # The recurrence: dp[i][j] = min(dp[i-1][j-1] + cost, dp[i-1][j] + 1, dp[i][j-1] + 1)
        # So at position (i,j) we can look at dp[i+1][j+1] etc.
        # Actually we need to look at dp[i][j] (already computed) and see which move leads to dp[i+1][j+1] etc.
        # Let's do backtracking but build ops forward.
        # We'll start at (0,0) and move to (n,m).
        # At each step, check which move is optimal.
        # We'll use parent table.
        # parent[i][j] tells how we got to (i,j) from previous.
        # But parent is for backward.
        # Let's compute forward parent: from (i,j) which next move is optimal.
        # We can compute by looking at dp[i][j] and dp[i+1][j+1] etc.
        # Simpler: we already have ops from backward pass but indices are wrong.
        # Let's just simulate forward with those ops and adjust indices.
        # We'll create a list of ops with indices relative to original a, then adjust.
        break
    
    # Let's do the simulation approach.
    # We have ops with indices relative to original a (before any operations).
    # We'll apply them sequentially while adjusting indices of later operations.
    # Because deletions and insertions shift indices.
    # We'll keep a mapping from original index to current index.
    # Actually we can process ops in order and adjust indices on the fly.
    # For each op, we need to know its index in the current string.
    # We'll maintain an offset list: for each position in original a, what is its current index after previous ops?
    # But deletions and insertions change length.
    # Better: simulate forward and adjust indices of remaining ops.
    
    # Let's implement simpler: compute operations directly with forward DP and track current indices.
    # We'll use dp table to decide moves.
    # At each step (i,j) we decide operation based on dp[i+1][j+1] etc.
    # We'll compute dp for whole strings, then walk forward.
    
    # Recompute dp with dimensions (n+1)*(m+1) as before.
    # Now walk from (0,0) to (n,m).
    ops = []
    i, j = 0, 0
    while i < n or j < m:
        if i < n and j < m and a[i] == b[j]:
            # match
            i += 1
            j += 1
            continue
        # Determine optimal operation
        # Check delete
        if i < n and dp[i+1][j] == dp[i][j] + 1:
            ops.append(('delete', i))
            i += 1
        # Check insert
        elif j < m and dp[i][j+1] == dp[i][j] + 1:
            ops.append(('insert', i, b[j]))
            j += 1
        # Check substitute
        elif i < n and j < m and dp[i+1][j+1] == dp[i][j] + 1:
            ops.append(('sub', i, b[j]))
            i += 1
            j += 1
        else:
            # Should not happen
            break
    
    return ops