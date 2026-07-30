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
        if open_count == n and close_count == n:
            result.append(current)
            return
        
        # Add an opening parenthesis if we haven't used all n
        if open_count < n:
            backtrack(current + '(', open_count + 1, close_count)
        
        # Add a closing parenthesis if it doesn't exceed opening parentheses
        if close_count < open_count:
            backtrack(current + ')', open_count, close_count + 1)
    
    backtrack('', 0, 0)
    return result
