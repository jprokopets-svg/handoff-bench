def is_match(s: str, p: str) -> bool:
    """
    Determines if a given string matches a simple pattern language.
    
    Pattern rules:
    - '.' matches any single character
    - '*' matches zero or more of the preceding character
    - Regular characters match themselves
    
    Args:
        s: The string to match
        p: The pattern to match against
    
    Returns:
        True if the string matches the pattern, False otherwise
    """
    m, n = len(s), len(p)
    
    # dp[i][j] = True if s[0:i] matches p[0:j]
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    
    # Handle patterns that can match empty string (like a*, a*b*, etc.)
    for j in range(2, n + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 2]
    
    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == '*':
                # Star case: matches zero or more of preceding character
                # Zero matches: dp[i][j-2] (skip the char and the star)
                dp[i][j] = dp[i][j - 2]
                
                # One or more matches: check if preceding char matches current string char
                if p[j - 2] == '.' or p[j - 2] == s[i - 1]:
                    # If it matches, we can consume this character and stay at same pattern position
                    dp[i][j] = dp[i][j] or dp[i - 1][j]
            else:
                # Non-star case: must match exactly
                if p[j - 1] == '.' or p[j - 1] == s[i - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
    
    return dp[m][n]
