def is_match(string, pattern):
    """
    Determines if a given string matches a simple pattern language.
    '.' matches any single character
    '*' matches zero or more of the preceding character
    
    Args:
        string: The string to match
        pattern: The pattern to match against
    
    Returns:
        True if the string matches the pattern, False otherwise
    """
    memo = {}
    
    def dp(i, j):
        # i is the index in string, j is the index in pattern
        # Returns True if string[i:] matches pattern[j:]
        
        if (i, j) in memo:
            return memo[(i, j)]
        
        # Base cases
        if j == len(pattern):
            # Pattern exhausted - match only if string is also exhausted
            result = (i == len(string))
        elif i == len(string):
            # String exhausted - pattern must be able to match empty string
            # This means remaining pattern must be of form: a*b*c* etc.
            result = True
            k = j
            while k < len(pattern):
                if k + 1 < len(pattern) and pattern[k + 1] == '*':
                    k += 2
                else:
                    result = False
                    break
        else:
            # Both string and pattern have characters left
            if j + 1 < len(pattern) and pattern[j + 1] == '*':
                # Next character in pattern is '*'
                # Option 1: Match zero occurrences of pattern[j]
                result = dp(i, j + 2)
                
                # Option 2: Match one or more occurrences of pattern[j]
                # We need to check if current char matches
                if not result and (pattern[j] == '.' or pattern[j] == string[i]):
                    result = dp(i + 1, j)
            else:
                # Next character in pattern is not '*'
                if pattern[j] == '.' or pattern[j] == string[i]:
                    result = dp(i + 1, j + 1)
                else:
                    result = False
        
        memo[(i, j)] = result
        return result
    
    return dp(0, 0)
