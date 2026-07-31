def is_match(s: str, p: str) -> bool:
    """
    Determines if string s matches pattern p.
    '.' matches any single character.
    '*' matches zero or more of the preceding character.
    
    Args:
        s: The input string to match.
        p: The pattern string containing '.', '*', and literal characters.
    
    Returns:
        True if s matches p, False otherwise.
    """
    # Use dynamic programming
    # dp[i][j] = True if s[:i] matches p[:j]
    m, n = len(s), len(p)
    
    # Create a (m+1) x (n+1) DP table
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    
    # Empty string matches empty pattern
    dp[0][0] = True
    
    # Handle patterns like a*, a*b*, a*b*c* that can match empty string
    for j in range(1, n + 1):
        if p[j - 1] == '*':
            # '*' can eliminate the preceding character (zero occurrences)
            dp[0][j] = dp[0][j - 2] if j >= 2 else False
    
    # Fill the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == '*':
                # Zero occurrences of preceding char: ignore "x*" in pattern
                zero_occ = dp[i][j - 2] if j >= 2 else False
                # One or more occurrences: preceding char matches s[i-1]
                if j >= 2 and (p[j - 2] == '.' or p[j - 2] == s[i - 1]):
                    one_or_more = dp[i - 1][j]
                else:
                    one_or_more = False
                dp[i][j] = zero_occ or one_or_more
            elif p[j - 1] == '.' or p[j - 1] == s[i - 1]:
                # Current characters match
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = False
    
    return dp[m][n]
