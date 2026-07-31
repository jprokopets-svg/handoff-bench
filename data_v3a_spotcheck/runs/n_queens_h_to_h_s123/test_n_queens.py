from n_queens import *


assert len(solve_n_queens(4)) == 2

assert len(solve_n_queens(1)) == 1

assert all(len(row) == 4 for sol in solve_n_queens(4) for row in sol)

assert all(row.count('Q') == 1 for sol in solve_n_queens(4) for row in sol)