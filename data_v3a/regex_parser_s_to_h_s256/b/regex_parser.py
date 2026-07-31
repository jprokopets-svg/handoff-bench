def is_match(s: str, p: str) -> bool:
    """
    Determine if string `s` matches pattern `p`.
    
    Pattern rules:
      '.' matches any single character.
      '*' matches zero or more of the preceding character.
    
    The match must cover the entire input string.
    
    Args:
        s: The input string to test.
        p: The pattern string (may contain '.' and '*').
    
    Returns:
        True if `s` fully matches `p`, False otherwise.
    """
    # Use dynamic programming
    # dp[i][j] = True if s[:i] matches p[:j]
    m, n = len(s), len(p)
    
    # dp table with (m+1) x (n+1)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    
    # Empty string matches empty pattern
    dp[0][0] = True
    
    # Empty string can match patterns like a*, a*b*, a*b*c*, etc.
    for j in range(1, n + 1):
        if p[j - 1] == '*':
            # '*' can eliminate the preceding element (zero occurrences)
            dp[0][j] = dp[0][j - 2] if j >= 2 else False
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            pc = p[j - 1]  # current pattern character
            
            if pc == '*':
                # '*' must have a preceding character in the pattern
                if j < 2:
                    dp[i][j] = False
                else:
                    prev_pc = p[j - 2]  # the character before '*'
                    # Option 1: zero occurrences of prev_pc — ignore "prev_pc*"
                    zero_match = dp[i][j - 2]
                    # Option 2: one or more occurrences — prev_pc matches s[i-1]
                    one_more = dp[i - 1][j] and (prev_pc == '.' or prev_pc == s[i - 1])
                    dp[i][j] = zero_match or one_more
            elif pc == '.':
                # '.' matches any single character
                dp[i][j] = dp[i - 1][j - 1]
            else:
                # Literal character match
                dp[i][j] = dp[i - 1][j - 1] and (pc == s[i - 1])
    
    return dp[m][n]
