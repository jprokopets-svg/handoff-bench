def min_edit_ops(a: str, b: str):
    """Return a minimal sequence of edit operations to transform a into b.

    Operations are tuples:
      ('delete', i)
      ('insert', i, c)
      ('sub', i, c)

    Indices refer to the current string state as operations are applied sequentially.
    """
    m, n = len(a), len(b)
    # dp table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if a[i-1] == b[j-1] else 1
            dp[i][j] = min(dp[i-1][j] + 1, dp[i][j-1] + 1, dp[i-1][j-1] + cost)
    # backtrace
    i, j = m, n
    ops_rev = []
    while i > 0 or j > 0:
        if i > 0 and j > 0 and a[i-1] == b[j-1] and dp[i][j] == dp[i-1][j-1]:
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i-1][j-1] + 1:
            # substitute a[i-1] -> b[j-1]
            ops_rev.append(('sub', i-1, b[j-1]))
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i-1][j] + 1:
            # delete a[i-1]
            ops_rev.append(('delete', i-1))
            i -= 1
        else:
            # insert b[j-1] at position i
            ops_rev.append(('insert', i, b[j-1]))
            j -= 1
    # ops_rev is from end->start; reverse to get forward sequence
    ops = list(reversed(ops_rev))
    return ops
