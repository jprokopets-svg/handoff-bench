from typing import List, Tuple


def min_edit_ops(a: str, b: str) -> List[Tuple]:
    """
    Return a minimal sequence of edit operations to transform a into b.
    Operations are of form ('delete', i), ('insert', i, c), ('sub', i, c)
    and indices refer to the current string state as operations are applied sequentially.
    """
    m, n = len(a), len(b)
    # Quick cases
    if a == b:
        return []
    # Build DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1,  # delete
                           dp[i][j - 1] + 1,  # insert
                           dp[i - 1][j - 1] + cost)  # sub or match
    # Backtrack to get operations in reverse (from end to start)
    ops_rev = []  # will store tuples like ('delete', orig_index) or ('insert', orig_index, char) or ('sub', orig_index, char)
    i, j = m, n
    while i > 0 or j > 0:
        # match or substitution
        if i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + (0 if a[i - 1] == b[j - 1] else 1):
            if a[i - 1] != b[j - 1]:
                ops_rev.append(('sub', i - 1, b[j - 1]))
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            # deletion of a[i-1]
            ops_rev.append(('delete', i - 1))
            i -= 1
        elif j > 0 and dp[i][j] == dp[i][j - 1] + 1:
            # insertion of b[j-1] at position i (before original index i)
            ops_rev.append(('insert', i, b[j - 1]))
            j -= 1
        else:
            # Fallback: if none matched due to ties, try sensible choices
            if i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
                ops_rev.append(('sub', i - 1, b[j - 1]))
                i -= 1
                j -= 1
            elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
                ops_rev.append(('delete', i - 1))
                i -= 1
            elif j > 0 and dp[i][j] == dp[i][j - 1] + 1:
                ops_rev.append(('insert', i, b[j - 1]))
                j -= 1
            else:
                # Shouldn't happen, but break to avoid infinite loop
                break
    # Reverse to get operations in forward application order
    ops_orig = list(reversed(ops_rev))

    # Map original-index-based ops to sequential indices by simulating application on a
    s = list(a)
    orig_indices: List = list(range(m))  # maps current positions to original indices; inserted chars have None
    result_ops: List[Tuple] = []

    for op in ops_orig:
        if op[0] == 'delete':
            orig_idx = op[1]
            # find position of this original index in current string
            try:
                pos = orig_indices.index(orig_idx)
            except ValueError:
                # If original index not present (already deleted), skip
                # This should not happen in a correct backtrack, but guard anyway
                continue
            # apply delete
            del s[pos]
            del orig_indices[pos]
            result_ops.append(('delete', pos))
        elif op[0] == 'sub':
            orig_idx, ch = op[1], op[2]
            try:
                pos = orig_indices.index(orig_idx)
            except ValueError:
                # If original index not present, cannot substitute; skip
                continue
            s[pos] = ch
            result_ops.append(('sub', pos, ch))
        else:  # insert
            orig_idx, ch = op[1], op[2]
            # find first position in orig_indices with value >= orig_idx
            pos = len(s)
            found = False
            for k, v in enumerate(orig_indices):
                # v may be None for previously inserted characters; treat None as greater than any orig_idx
                if v is None:
                    continue
                if v >= orig_idx:
                    pos = k
                    found = True
                    break
            if not found:
                pos = len(s)
            s.insert(pos, ch)
            orig_indices.insert(pos, None)
            result_ops.append(('insert', pos, ch))
    return result_ops
