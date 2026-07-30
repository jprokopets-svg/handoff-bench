def generate_parentheses(n: int) -> list[str]:
    """
    Generate all valid combinations of n pairs of parentheses.
    
    Args:
        n: Number of pairs of parentheses
        
    Returns:
        A list of all valid combinations of n pairs of parentheses
    """
    result = []
    
    def backtrack(current: str, open_count: int, close_count: int):
        """
        Recursively build valid parentheses combinations.
        
        Args:
            current: Current string being built
            open_count: Number of opening parentheses used
            close_count: Number of closing parentheses used
        """
        # Base case: we've used all n pairs
        if open_count == n and close_count == n:
            result.append(current)
            return
        
        # Add opening parenthesis if we haven't used all n
        if open_count < n:
            backtrack(current + '(', open_count + 1, close_count)
        
        # Add closing parenthesis if we have more opening than closing
        if close_count < open_count:
            backtrack(current + ')', open_count, close_count + 1)
    
    backtrack('', 0, 0)
    return result
