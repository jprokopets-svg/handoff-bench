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
    cols = set()
    diag1 = set()  # row - col
    diag2 = set()  # row + col
    
    def backtrack(row):
        if row == n:
            # Found a valid solution, add it to solutions
            solutions.append([''.join(board[i]) for i in range(n)])
            return
        
        for col in range(n):
            # Check if this position is safe
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            
            # Place queen
            board[row][col] = 'Q'
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            
            # Recurse to next row
            backtrack(row + 1)
            
            # Remove queen (backtrack)
            board[row][col] = '.'
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)
    
    backtrack(0)
    return solutions
