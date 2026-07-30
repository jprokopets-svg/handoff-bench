def is_match(s, p):
    """
    Determine if string s matches pattern p.
    
    Pattern rules:
    - '.' matches any single character
    - '*' matches zero or more of the preceding character
    
    Args:
        s: The string to match
        p: The pattern to match against
    
    Returns:
        True if s matches p, False otherwise
    """
    # Dynamic programming approach
    # dp[i][j] = True if s[0:i] matches p[0:j]
    
    m, n = len(s), len(p)
    
    # Create DP table
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
                # Case 1: Match zero occurrences - skip the char and *
                dp[i][j] = dp[i][j - 2]
                
                # Case 2: Match one or more occurrences
                # Check if the character before * matches current char in s
                if p[j - 2] == '.' or p[j - 2] == s[i - 1]:
                    # If previous state matched, we can extend by matching one more
                    dp[i][j] = dp[i][j] or dp[i - 1][j]
            else:
                # Current pattern character is either '.' or a literal
                if p[j - 1] == '.' or p[j - 1] == s[i - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
    
    # Debug: print the DP table for the failing case
    if s == "mississippi" and p == "mis*is*p*.":
        print("\nDP Table for failing case:")
        print("s =", s)
        print("p =", p)
        print("\nDP table:")
        print("    ", " ".join(f"{c:2}" for c in " " + p))
        for i in range(m + 1):
            row_label = " " if i == 0 else s[i - 1]
            print(f"{row_label:2}  ", " ".join(f"{int(dp[i][j]):2}" for j in range(n + 1)))
    
    return dp[m][n]
