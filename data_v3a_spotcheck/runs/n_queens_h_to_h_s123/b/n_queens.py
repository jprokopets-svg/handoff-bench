def solveNQueens(n):
    """
    Solve the N-Queens problem and return all distinct solutions.
    Each solution is a list of strings where 'Q' marks a queen and '.' marks empty.
    
    Args:
        n: The size of the chessboard (n x n)
    
    Returns:
        A list of solutions, where each solution is a list of strings representing the board
    """
    solutions = []
    board = []
    
    def is_safe(row, col):
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
    
    def backtrack(row):
        """Backtracking function to place queens"""
        if row == n:
            # Found a valid solution, convert to string format
            solution = []
            for col in board:
                line = ['.' for _ in range(n)]
                line[col] = 'Q'
                solution.append(''.join(line))
            solutions.append(solution)
            return
        
        # Try placing a queen in each column of the current row
        for col in range(n):
            if is_safe(row, col):
                board.append(col)
                backtrack(row + 1)
                board.pop()
    
    backtrack(0)
    return solutions
