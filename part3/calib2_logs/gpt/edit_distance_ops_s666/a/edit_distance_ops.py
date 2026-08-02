def min_edit_ops(a: str, b: str):
    """Return a minimal sequence of edit operations to transform a into b.

    Operations are tuples:
      ('delete', i)         -- delete char at index i
      ('insert', i, c)      -- insert char c at index i
      ('sub', i, c)         -- substitute char at index i with c

    Indices refer to the current string state after prior operations (i.e. apply ops in order).
    """
    la = len(a)
    lb = len(b)
    # DP table
    dp = [[0] * (lb + 1) for _ in range(la + 1)]
    for i in range(la + 1):
        dp[i][0] = i
    for j in range(lb + 1):
        dp[0][j] = j
    for i in range(1, la + 1):
        ai = a[i-1]
        for j in range(1, lb + 1):
            cost = 0 if ai == b[j-1] else 1
            dp[i][j] = min(dp[i-1][j] + 1,      # delete
                           dp[i][j-1] + 1,      # insert
                           dp[i-1][j-1] + cost) # substitute/match
    # Backtrack to produce operations (in reverse, indices relative to original a positions)
    ops_rev = []
    i, j = la, lb
    while i > 0 or j > 0:
        if i > 0 and j > 0 and dp[i][j] == dp[i-1][j-1] + (0 if a[i-1] == b[j-1] else 1):
            # match or substitute
            if a[i-1] != b[j-1]:
                # substitute at position i-1 (original index)
                ops_rev.append(('sub', i-1, b[j-1]))
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i-1][j] + 1:
            # deletion of a[i-1]
            ops_rev.append(('delete', i-1))
            i -= 1
        else:
            # insertion of b[j-1] at position i (original index where to insert)
            ops_rev.append(('insert', i, b[j-1]))
            j -= 1
    # reverse to get forward order (indices currently refer to original a positions)
    ops_orig = list(reversed(ops_rev))
    # Adjust indices so they refer to the current string state as ops are applied sequentially.
    final_ops = []
    offset = 0
    for op in ops_orig:
        if op[0] == 'delete':
            idx_orig = op[1]
            idx = idx_orig + offset
            final_ops.append(('delete', idx))
            offset -= 1
        elif op[0] == 'insert':
            idx_orig = op[1]
            c = op[2]
            idx = idx_orig + offset
            final_ops.append(('insert', idx, c))
            offset += 1
        else:  # sub
            idx_orig = op[1]
            c = op[2]
            idx = idx_orig + offset
            final_ops.append(('sub', idx, c))
    return final_ops
