def min_edit_ops(a: str, b: str) -> list[tuple]:
    """Return a minimal sequence of edit operations transforming a into b.

    Operations are ('delete', i), ('insert', i, c), ('sub', i, c) and apply
    sequentially to the current string. The sequence length equals the
    Levenshtein distance.
    """
    m, n = len(a), len(b)
    # dp[i][j] = edit distance from a[i:] to b[j:]
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m, -1, -1):
        for j in range(n, -1, -1):
            if i == m and j == n:
                dp[i][j] = 0
            elif i == m:
                dp[i][j] = n - j
            elif j == n:
                dp[i][j] = m - i
            else:
                if a[i] == b[j]:
                    dp[i][j] = dp[i+1][j+1]
                else:
                    dp[i][j] = 1 + min(dp[i+1][j], dp[i][j+1], dp[i+1][j+1])
    # Build operations by simulating forward using dp decisions
    s = list(a)
    ops: list[tuple] = []
    i = 0
    j = 0
    pos = 0  # current index in s corresponding to a[i]
    while i < m or j < n:
        if i < m and j < n and a[i] == b[j]:
            # no operation needed
            i += 1
            j += 1
            pos += 1
            continue
        # If we've exhausted a, must insert remaining b's
        if i == m:
            # insert b[j] at pos
            ops.append(('insert', pos, b[j]))
            s.insert(pos, b[j])
            j += 1
            pos += 1
            continue
        # If we've exhausted b, must delete remaining a's
        if j == n:
            ops.append(('delete', pos))
            del s[pos]
            i += 1
            # pos remains same because next char shifted into this index
            continue
        # otherwise choose operation that matches dp
        # substitution
        if dp[i][j] == 1 + dp[i+1][j+1]:
            ops.append(('sub', pos, b[j]))
            s[pos] = b[j]
            i += 1
            j += 1
            pos += 1
        elif dp[i][j] == 1 + dp[i+1][j]:
            # delete a[i]
            ops.append(('delete', pos))
            del s[pos]
            i += 1
            # pos stays
        else:
            # insert b[j]
            ops.append(('insert', pos, b[j]))
            s.insert(pos, b[j])
            j += 1
            pos += 1
    return ops
