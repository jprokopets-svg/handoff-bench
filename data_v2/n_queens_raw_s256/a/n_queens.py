def solveNQueens(n):
    """
    Return all distinct solutions to the N-Queens problem.
    Each solution is a list of strings where 'Q' marks a queen and '.' marks empty.
    
    Args:
        n: The size of the chessboard (n x n)
    
    Returns:
        A list of solutions, where each solution is a list of strings representing the board
    """
    solutions = []
    board = []
    cols = set()
    diag1 = set()  # row - col
    diag2 = set()  # row + col
    
    def backtrack(row):
        # Base case: all queens placed successfully
        if row == n:
            solutions.append([''.join(row_config) for row_config in board])
            return
        
        # Try placing a queen in each column of the current row
        for col in range(n):
            # Check if this position is safe
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            
            # Place the queen
            row_config = ['.' for _ in range(n)]
            row_config[col] = 'Q'
            board.append(row_config)
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            
            # Recurse to the next row
            backtrack(row + 1)
            
            # Remove the queen (backtrack)
            board.pop()
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)
    
    backtrack(0)
    return solutions
