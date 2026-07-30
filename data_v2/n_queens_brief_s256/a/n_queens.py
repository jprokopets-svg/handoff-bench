def solveNQueens(n):
    """
    Solve the N-Queens problem and return all distinct solutions.
    
    Each solution is a list of strings where 'Q' marks a queen and '.' marks empty.
    
    Args:
        n: The size of the board (n x n)
    
    Returns:
        A list of all distinct solutions, where each solution is a list of strings
    """
    results = []
    
    def is_safe(board, row, col):
        """Check if placing a queen at (row, col) is safe"""
        # Check column
        for i in range(row):
            if board[i] == col:
                return False
        
        # Check upper left diagonal
        for i in range(row):
            if abs(board[i] - col) == abs(i - row):
                return False
        
        return True
    
    def backtrack(board, row):
        """Backtrack to find all valid solutions"""
        if row == n:
            # Found a valid solution
            solution = []
            for col in board:
                line = '.' * col + 'Q' + '.' * (n - col - 1)
                solution.append(line)
            results.append(solution)
            return
        
        # Try placing a queen in each column of the current row
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                backtrack(board, row + 1)
                board[row] = -1
    
    # Initialize board: board[i] represents the column position of queen in row i
    board = [-1] * n
    backtrack(board, 0)
    
    return results
