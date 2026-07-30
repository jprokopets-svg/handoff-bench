def solveNQueens(n):
    """
    Solve the N-Queens problem and return all distinct solutions.
    
    Args:
        n: The size of the board (n x n)
    
    Returns:
        A list of solutions, where each solution is a list of strings.
        'Q' represents a queen and '.' represents an empty space.
    """
    solutions = []
    board = [['.' for _ in range(n)] for _ in range(n)]
    cols = set()
    diag1 = set()  # row - col
    diag2 = set()  # row + col
    
    def backtrack(row):
        if row == n:
            # Found a valid solution, add it to solutions
            solution = [''.join(row_list) for row_list in board]
            solutions.append(solution)
            return
        
        for col in range(n):
            # Check if placing a queen at (row, col) is safe
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            
            # Place the queen
            board[row][col] = 'Q'
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            
            # Recurse to the next row
            backtrack(row + 1)
            
            # Remove the queen (backtrack)
            board[row][col] = '.'
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)
    
    backtrack(0)
    return solutions
