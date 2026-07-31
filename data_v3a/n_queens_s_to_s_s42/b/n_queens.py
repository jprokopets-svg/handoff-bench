def solve_n_queens(n):
    """
    Returns all distinct solutions to the N-Queens problem.
    Each solution is a list of strings where 'Q' marks a queen and '.' marks empty.
    """
    results = []

    def backtrack(row, cols, diag1, diag2, placement):
        if row == n:
            board = []
            for col in placement:
                board.append('.' * col + 'Q' + '.' * (n - col - 1))
            results.append(board)
            return

        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            placement.append(col)

            backtrack(row + 1, cols, diag1, diag2, placement)

            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)
            placement.pop()

    backtrack(0, set(), set(), set(), [])
    return results
