def generate_parentheses(n):
    """
    Generate all valid combinations of n pairs of parentheses.
    
    Args:
        n: Number of pairs of parentheses
        
    Returns:
        A list of all valid combinations of n pairs of parentheses
    """
    result = []
    
    def backtrack(current, open_count, close_count):
        # Base case: we've used all n pairs
        if len(current) == 2 * n:
            result.append(current)
            return
        
        # Add opening parenthesis if we haven't used all n opening parentheses
        if open_count < n:
            backtrack(current + '(', open_count + 1, close_count)
        
        # Add closing parenthesis if we have more opening than closing
        if close_count < open_count:
            backtrack(current + ')', open_count, close_count + 1)
    
    backtrack('', 0, 0)
    return result
