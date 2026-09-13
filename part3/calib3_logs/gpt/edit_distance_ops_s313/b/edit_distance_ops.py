def min_edit_ops(a: str, b: str):
    """Return a minimal sequence of edit operations to transform a into b.

    Operations are tuples:
      ('delete', i)
      ('insert', i, c)
      ('sub', i, c)

    Indices refer to the current string state as operations are applied sequentially.
    """
    m, n = len(a), len(b)
    # dp[i][j] = min edits to convert a[:i] -> b[:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if a[i-1] == b[j-1] else 1
            dp[i][j] = min(dp[i-1][j] + 1, dp[i][j-1] + 1, dp[i-1][j-1] + cost)

    ops = []
    i = 0
    j = 0
    # Walk forward through prefixes, emitting operations with indices that refer to current string
    while i < m or j < n:
        # When both characters remain
        if i < m and j < n:
            # match (no operation)
            if a[i] == b[j] and dp[i+1][j+1] == dp[i][j]:
                i += 1
                j += 1
                continue
            # substitution
            if dp[i+1][j+1] == dp[i][j] + 1:
                ops.append(('sub', i, b[j]))
                i += 1
                j += 1
                continue
            # deletion
            if dp[i+1][j] == dp[i][j] + 1:
                ops.append(('delete', i))
                i += 1
                continue
            # insertion
            if dp[i][j+1] == dp[i][j] + 1:
                ops.append(('insert', i, b[j]))
                j += 1
                continue
            # fallback (shouldn't happen)
            raise RuntimeError('No valid forward transition at i=%d j=%d' % (i, j))
        elif i < m:
            # must delete remaining
            ops.append(('delete', i))
            i += 1
        else:
            # j < n, must insert remaining
            ops.append(('insert', i, b[j]))
            j += 1
    return ops
