def solveNQueens(n):
    """
    Solve the N-Queens problem and return all distinct solutions.
    
    Args:
        n: The size of the chessboard (n x n)
    
    Returns:
        A list of solutions, where each solution is a list of strings
        representing the board configuration with 'Q' for queens and '.' for empty spaces.
    """
    solutions = []
    board = [['.' for _ in range(n)] for _ in range(n)]
    
    def is_safe(current_row, col):
        """Check if placing a queen at (current_row, col) is safe."""
        # Check column
        for i in range(current_row):
            if board[i][col] == 'Q':
                return False
        
        # Check upper left diagonal
        i, j = current_row - 1, col - 1
        while i >= 0 and j >= 0:
            if board[i][j] == 'Q':
                return False
            i -= 1
            j -= 1
        
        # Check upper right diagonal
        i, j = current_row - 1, col + 1
        while i >= 0 and j < n:
            if board[i][j] == 'Q':
                return False
            i -= 1
            j += 1
        
        return True
    
    def backtrack(current_row):
        """Recursively place queens using backtracking."""
        if current_row == n:
            # Found a valid solution, add it to solutions
            solutions.append([''.join(row_list) for row_list in board])
            return
        
        for col in range(n):
            if is_safe(current_row, col):
                board[current_row][col] = 'Q'
                backtrack(current_row + 1)
                board[current_row][col] = '.'
    
    backtrack(0)
    return solutions
