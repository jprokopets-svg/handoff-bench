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
    board = [['.' for _ in range(n)] for _ in range(n)]
    
    def is_safe(row, col):
        """Check if placing a queen at (row, col) is safe."""
        # Check column
        for i in range(row):
            if board[i][col] == 'Q':
                return False
        
        # Check upper left diagonal
        i, j = row - 1, col - 1
        while i >= 0 and j >= 0:
            if board[i][j] == 'Q':
                return False
            i -= 1
            j -= 1
        
        # Check upper right diagonal
        i, j = row - 1, col + 1
        while i >= 0 and j < n:
            if board[i][j] == 'Q':
                return False
            i -= 1
            j += 1
        
        return True
    
    def backtrack(row):
        """Recursively place queens row by row."""
        if row == n:
            # Found a valid solution, add it to results
            solution = [''.join(row) for row in board]
            results.append(solution)
            return
        
        for col in range(n):
            if is_safe(row, col):
                board[row][col] = 'Q'
                backtrack(row + 1)
                board[row][col] = '.'
    
    backtrack(0)
    return results
