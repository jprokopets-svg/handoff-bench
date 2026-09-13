def min_edit_ops(a: str, b: str) -> list[tuple]:
    m = len(a)
    n = len(b)
    # dp[i][j] = distance from a[i:] to b[j:]
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    # base cases
    for i in range(m + 1):
        dp[i][n] = m - i
    for j in range(n + 1):
        dp[m][j] = n - j
    # fill
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            if a[i] == b[j]:
                dp[i][j] = dp[i + 1][j + 1]
            else:
                dp[i][j] = 1 + min(dp[i + 1][j + 1], dp[i + 1][j], dp[i][j + 1])
    # simulate forward to produce operations applied to current string
    ops = []
    s = list(a)
    i = j = 0
    pos = 0
    while i < m or j < n:
        # if both remain and characters match, advance
        if i < m and j < n and a[i] == b[j]:
            i += 1
            j += 1
            pos += 1
            continue
        # If substitution is optimal
        if i < m and j < n and dp[i][j] == dp[i + 1][j + 1] + 1:
            ops.append(('sub', pos, b[j]))
            # apply
            s[pos] = b[j]
            i += 1
            j += 1
            pos += 1
            continue
        # If deletion is optimal
        if i < m and dp[i][j] == dp[i + 1][j] + 1:
            ops.append(('delete', pos))
            del s[pos]
            i += 1
            # pos stays the same
            continue
        # Otherwise insertion must be optimal
        if j < n and dp[i][j] == dp[i][j + 1] + 1:
            ops.append(('insert', pos, b[j]))
            s.insert(pos, b[j])
            j += 1
            pos += 1
            continue
        # Fallback (shouldn't happen)
        break
    return ops
