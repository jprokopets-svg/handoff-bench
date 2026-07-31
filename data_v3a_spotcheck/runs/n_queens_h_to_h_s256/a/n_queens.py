def solveNQueens(n):
    """
    Solve the N-Queens problem and return all distinct solutions.
    
    Args:
        n: The size of the board (n x n)
    
    Returns:
        A list of solutions, where each solution is a list of strings
        representing the board with 'Q' for queens and '.' for empty spaces.
    """
    solutions = []
    
    def is_safe(board, row, col):
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
    
    def backtrack(board, row):
        """Recursively place queens and find all solutions."""
        if row == n:
            # Found a valid solution, convert board to list of strings
            solutions.append([''.join(row_list) for row_list in board])
            return
        
        for col in range(n):
            if is_safe(board, row, col):
                board[row][col] = 'Q'
                backtrack(board, row + 1)
                board[row][col] = '.'
    
    # Initialize the board with all empty spaces
    board = [['.' for _ in range(n)] for _ in range(n)]
    backtrack(board, 0)
    
    return solutions
