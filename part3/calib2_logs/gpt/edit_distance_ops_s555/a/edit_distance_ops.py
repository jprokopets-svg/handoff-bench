def min_edit_ops(a: str, b: str):
    """Return a minimal sequence of edit operations to transform a into b.
    Operations: ('delete', i), ('insert', i, c), ('sub', i, c).
    Indices refer to the current string state when the operation is applied.
    """
    m = len(a)
    n = len(b)
    # build dp table: cost to convert a[:i] -> b[:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost_sub = dp[i-1][j-1] + (0 if a[i-1] == b[j-1] else 1)
            cost_del = dp[i-1][j] + 1
            cost_ins = dp[i][j-1] + 1
            dp[i][j] = min(cost_sub, cost_del, cost_ins)
    # backtrack to get operations in reverse (from end to start)
    i = m
    j = n
    ops_rev = []  # in reverse application order, positions refer to original a indices
    while i > 0 or j > 0:
        if i > 0 and j > 0 and dp[i][j] == dp[i-1][j-1] and a[i-1] == b[j-1]:
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i-1][j-1] + 1:
            # substitution of a[i-1] -> b[j-1]
            ops_rev.append(('sub', i-1, b[j-1]))
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i-1][j] + 1:
            # delete a[i-1]
            ops_rev.append(('delete', i-1))
            i -= 1
        else:
            # insertion of b[j-1] at position i (between a[i-1] and a[i])
            ops_rev.append(('insert', i, b[j-1]))
            j -= 1
    # reverse to get forward application order
    ops_forward = list(reversed(ops_rev))
    # Now convert original-index-based ops to indices valid for sequential application.
    s = list(a)
    orig_indices = list(range(m))  # for each character in s, store its original index; inserted chars get None
    result_ops = []
    for op in ops_forward:
        if op[0] == 'delete':
            orig_pos = op[1]
            # find index in current s whose original index equals orig_pos
            try:
                idx = orig_indices.index(orig_pos)
            except ValueError:
                # Should not happen
                idx = len(s)
            # perform delete
            del s[idx]
            del orig_indices[idx]
            result_ops.append(('delete', idx))
        elif op[0] == 'sub':
            orig_pos = op[1]
            ch = op[2]
            try:
                idx = orig_indices.index(orig_pos)
            except ValueError:
                idx = len(s)
            s[idx] = ch
            result_ops.append(('sub', idx, ch))
        else:  # insert
            orig_pos = op[1]
            ch = op[2]
            # find first index in orig_indices with value >= orig_pos
            idx = None
            for k, v in enumerate(orig_indices):
                if v is None:
                    # inserted chars - treat them as having no original pos; they should come after previous inserts
                    # we don't count them for locating insertion point
                    continue
                if v >= orig_pos:
                    idx = k
                    break
            if idx is None:
                idx = len(s)
            s.insert(idx, ch)
            orig_indices.insert(idx, None)
            result_ops.append(('insert', idx, ch))
    return result_ops
