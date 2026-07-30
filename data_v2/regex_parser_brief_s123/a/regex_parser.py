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
    memo = {}
    
    def dp(i, j):
        # i is the index in string s, j is the index in pattern p
        
        # Base cases
        if (i, j) in memo:
            return memo[(i, j)]
        
        # If we've consumed the entire pattern
        if j == len(p):
            result = i == len(s)
            memo[(i, j)] = result
            return result
        
        # Check if current characters match
        first_match = i < len(s) and (p[j] == '.' or p[j] == s[i])
        
        # Check if next character in pattern is '*'
        if j + 1 < len(p) and p[j + 1] == '*':
            # Two options:
            # 1. Skip this pattern (zero matches of preceding char)
            # 2. Match current char and stay at same pattern position (one or more matches)
            result = dp(i, j + 2) or (first_match and dp(i + 1, j))
        else:
            # No '*' following, so we need to match current character
            result = first_match and dp(i + 1, j + 1)
        
        memo[(i, j)] = result
        return result
    
    return dp(0, 0)
