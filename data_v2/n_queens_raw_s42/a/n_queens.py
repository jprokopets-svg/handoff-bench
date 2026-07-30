def solveNQueens(n):
    """
    Returns all distinct solutions to the N-Queens problem.
    Each solution is a list of strings where 'Q' marks a queen and '.' marks empty.
    
    Args:
        n: The size of the chessboard (n x n)
    
    Returns:
        A list of solutions, where each solution is a list of strings representing the board
    """
    solutions = []
    
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
        """Backtracking function to place queens"""
        if row == n:
            # Found a valid solution
            solution = []
            for col in board:
                line = ['.' for _ in range(n)]
                line[col] = 'Q'
                solution.append(''.join(line))
            solutions.append(solution)
            return
        
        # Try placing queen in each column of current row
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                backtrack(board, row + 1)
                board[row] = -1
    
    # Initialize board: board[i] represents the column position of queen in row i
    board = [-1] * n
    backtrack(board, 0)
    
    return solutions
