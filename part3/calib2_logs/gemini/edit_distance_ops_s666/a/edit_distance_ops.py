
def min_edit_ops(a, b):
    n = len(a)
    m = len(b)

    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j],      # Delete
                                   dp[i][j - 1],      # Insert
                                   dp[i - 1][j - 1])  # Substitute

    operations = []
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and a[i - 1] == b[j - 1]:
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1: # Substitute
            operations.insert(0, ('sub', i - 1, b[j - 1]))
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1: # Delete
            operations.insert(0, ('delete', i - 1))
            i -= 1
        elif j > 0 and dp[i][j] == dp[i][j - 1] + 1: # Insert
            # The index for insert should be the current length of the string 'a' that has been processed.
            # When we insert, we are effectively inserting into the string 'a' at position 'i'.
            operations.insert(0, ('insert', i, b[j - 1]))
            j -= 1
    return operations
