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
    
    # backtrack to build operations (indices relative to original string)
    ops_backward = []
    i, j = n, m
    while i > 0 or j > 0:
        if parent[i][j] == 0:
            # substitution or match
            if a[i-1] != b[j-1]:
                # need substitution
                ops_backward.append(('sub', i-1, b[j-1]))
            i -= 1
            j -= 1
        elif parent[i][j] == 1:
            # delete a[i-1]
            ops_backward.append(('delete', i-1))
            i -= 1
        else:  # parent[i][j] == 2
            # insert b[j-1] at position i (after a[:i])
            ops_backward.append(('insert', i, b[j-1]))
            j -= 1
    
    # ops_backward are built backwards, reverse to get order relative to original string
    ops_backward.reverse()
    
    # Now adjust indices for sequential application
    # We'll simulate applying operations to a copy of the string
    # and track how indices shift due to deletions and insertions
    adjusted_ops = []
    # Track offset for each position in original string
    # offset[i] = how many positions character at original index i has shifted
    # We'll compute offsets dynamically as we process operations
    current_str = list(a)
    # Map from original index to current index
    # We'll process operations in order, adjusting indices based on previous operations
    
    # Instead of complex offset tracking, we can process operations sequentially
    # and adjust indices of future operations
    # We'll keep a list of operations with original indices, then adjust
    
    # Build a list of operations with original indices
    ops_original = ops_backward.copy()
    
    # Now adjust indices by simulating forward
    # We need to know for each operation what the current index is
    # We'll process operations in order, maintaining current string length
    # and adjusting indices of remaining operations
    
    # Create a copy of ops_original to modify
    ops_to_adjust = ops_original.copy()
    adjusted_ops = []
    
    # Track offset: how many positions have been inserted/deleted before current position
    offset = 0
    
    # Process operations in order
    for op in ops_to_adjust:
        if op[0] == 'delete':
            orig_idx = op[1]
            current_idx = orig_idx + offset
            adjusted_ops.append(('delete', current_idx))
            # Deletion reduces length, so offset decreases for subsequent positions
            # Actually, after deletion, indices of characters after the deleted position shift left by 1
            # So for future operations, we need to adjust offset
            offset -= 1
        elif op[0] == 'insert':
            orig_idx = op[1]
            current_idx = orig_idx + offset
            adjusted_ops.append(('insert', current_idx, op[2]))
            # Insertion increases length, so offset increases for subsequent positions
            offset += 1
        elif op[0] == 'sub':
            orig_idx = op[1]
            current_idx = orig_idx + offset
            adjusted_ops.append(('sub', current_idx, op[2]))
            # Substitution doesn't change length, offset stays the same
    
    return adjusted_ops