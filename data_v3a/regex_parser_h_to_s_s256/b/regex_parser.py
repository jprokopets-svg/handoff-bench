def matches(pattern, text):
    """
    Determines if a given string matches a simple pattern language.
    '.' matches any single character
    '*' matches zero or more of the preceding character
    
    Args:
        pattern: The regex pattern string
        text: The text to match against
        
    Returns:
        True if the text matches the pattern, False otherwise
    """
    # Dynamic programming approach with memoization
    memo = {}
    
    def dp(p_idx, t_idx):
        # Base cases
        if (p_idx, t_idx) in memo:
            return memo[(p_idx, t_idx)]
        
        # If pattern is exhausted
        if p_idx == len(pattern):
            result = t_idx == len(text)
            memo[(p_idx, t_idx)] = result
            return result
        
        # Check if current pattern char is followed by '*'
        has_star = p_idx + 1 < len(pattern) and pattern[p_idx + 1] == '*'
        
        if has_star:
            # Case 1: Match zero occurrences of the character (skip the char and *)
            if dp(p_idx + 2, t_idx):
                memo[(p_idx, t_idx)] = True
                return True
            
            # Case 2: Match one or more occurrences
            # Check if current char matches (either '.' or exact match)
            if t_idx < len(text) and (pattern[p_idx] == '.' or pattern[p_idx] == text[t_idx]):
                if dp(p_idx, t_idx + 1):
                    memo[(p_idx, t_idx)] = True
                    return True
        else:
            # No star following, must match exactly one character
            if t_idx < len(text) and (pattern[p_idx] == '.' or pattern[p_idx] == text[t_idx]):
                if dp(p_idx + 1, t_idx + 1):
                    memo[(p_idx, t_idx)] = True
                    return True
        
        memo[(p_idx, t_idx)] = False
        return False
    
    return dp(0, 0)
