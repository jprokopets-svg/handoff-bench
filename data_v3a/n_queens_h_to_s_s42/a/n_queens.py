def solveNQueens(n):
    """
    Solve the N-Queens problem and return all distinct solutions.
    
    Args:
        n: The size of the chessboard (n x n)
    
    Returns:
        A list of solutions, where each solution is a list of strings
        representing the board configuration with 'Q' for queens and '.' for empty spaces.
    """
    results = []
    
    def is_safe(board, row, col):
        """Check if placing a queen at (row, col) is safe."""
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
        """Recursively place queens using backtracking."""
        if row == n:
            # Found a valid solution, convert to string representation
            solution = []
            for i in range(n):
                line = ['.' for _ in range(n)]
                line[board[i]] = 'Q'
                solution.append(''.join(line))
            results.append(solution)
            return
        
        # Try placing queen in each column of current row
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                backtrack(board, row + 1)
                board[row] = -1
    
    # Initialize board: board[i] represents column position of queen in row i
    board = [-1] * n
    backtrack(board, 0)
    
    return results
