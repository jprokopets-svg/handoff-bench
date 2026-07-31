def solve_n_queens(n):
    """
    Returns all distinct solutions to the N-Queens problem.
    Each solution is a list of strings where 'Q' marks a queen and '.' marks empty.
    """
    results = []

    def is_valid(queens, row, col):
        for r, c in enumerate(queens):
            if c == col:
                return False
            if abs(r - row) == abs(c - col):
                return False
        return True

    def backtrack(row, queens):
        if row == n:
            # Build the board
            board = []
            for c in queens:
                board.append('.' * c + 'Q' + '.' * (n - c - 1))
            results.append(board)
            return
        for col in range(n):
            if is_valid(queens, row, col):
                queens.append(col)
                backtrack(row + 1, queens)
                queens.pop()

    backtrack(0, [])
    return results
