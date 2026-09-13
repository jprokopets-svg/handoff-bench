from edit_distance_ops import *


def _lev(a, b):
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a) + 1):
        dp[i][0] = i
    for j in range(len(b) + 1):
        dp[0][j] = j
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            dp[i][j] = min(dp[i-1][j] + 1, dp[i][j-1] + 1, dp[i-1][j-1] + (0 if a[i-1] == b[j-1] else 1))
    return dp[len(a)][len(b)]

def _replay(a, ops):
    s = list(a)
    for op in ops:
        if op[0] == 'delete':
            del s[op[1]]
        elif op[0] == 'insert':
            s.insert(op[1], op[2])
        else:
            s[op[1]] = op[2]
    return ''.join(s)

ops = min_edit_ops('kitten', 'sitting'); assert len(ops) == _lev('kitten', 'sitting') and _replay('kitten', ops) == 'sitting'

ops = min_edit_ops('', 'abc'); assert len(ops) == 3 and _replay('', ops) == 'abc'

ops = min_edit_ops('abc', ''); assert len(ops) == 3 and _replay('abc', ops) == ''

ops = min_edit_ops('abc', 'abc'); assert ops == [] and _replay('abc', ops) == 'abc'

ops = min_edit_ops('sunday', 'saturday'); assert len(ops) == _lev('sunday', 'saturday') and _replay('sunday', ops) == 'saturday'

ops = min_edit_ops('intention', 'execution'); assert len(ops) == _lev('intention', 'execution') and _replay('intention', ops) == 'execution'

ops = min_edit_ops('cat', 'cut'); assert len(ops) == 1 and _replay('cat', ops) == 'cut'