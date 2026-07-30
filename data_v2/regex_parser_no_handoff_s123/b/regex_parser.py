def is_match(s, p):
    """
    Determines if a given string matches a simple pattern.
    
    Pattern rules:
    - '.' matches any single character
    - '*' matches zero or more of the preceding character
    
    Args:
        s: The string to match
        p: The pattern to match against
        
    Returns:
        True if the string matches the pattern, False otherwise
    """
    # Create a DP table where dp[i][j] represents whether s[0:i] matches p[0:j]
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    
    # Empty string matches empty pattern
    dp[0][0] = True
    
    # Handle patterns like a*, a*b*, a*b*c* which can match empty string
    for j in range(2, n + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 2]
    
    # Fill the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == '*':
                # '*' matches zero or more of the preceding character
                # dp[i][j-2] means we match zero occurrences of the preceding char
                # dp[i-1][j] means we match one or more occurrences
                dp[i][j] = dp[i][j - 2]  # zero occurrences
                
                if p[j - 2] == '.' or p[j - 2] == s[i - 1]:
                    # If the preceding character matches current char in s
                    dp[i][j] = dp[i][j] or dp[i - 1][j]
            else:
                # Current character in pattern is either '.' or a literal character
                if p[j - 1] == '.' or p[j - 1] == s[i - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
    
    return dp[m][n]
