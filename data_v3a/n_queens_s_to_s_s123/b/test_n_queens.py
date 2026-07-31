from n_queens import solve_n_queens


def test_n1():
    assert solve_n_queens(1) == [["Q"]]


def test_n4_count():
    solutions = solve_n_queens(4)
    assert len(solutions) == 2


def test_n4_solutions():
    solutions = solve_n_queens(4)
    expected = sorted([
        [".Q..", "...Q", "Q...", "..Q."],
        ["..Q.", "Q...", "...Q", ".Q.."]
    ])
    assert sorted(solutions) == expected


def test_n8_count():
    solutions = solve_n_queens(8)
    assert len(solutions) == 92


def test_n0():
    # Edge case: 0 queens — one trivial solution (empty board)
    solutions = solve_n_queens(0)
    assert solutions == [[]]


def test_n2_no_solution():
    solutions = solve_n_queens(2)
    assert solutions == []


def test_n3_no_solution():
    solutions = solve_n_queens(3)
    assert solutions == []


def test_solution_format():
    """Each solution must be a list of n strings, each of length n with exactly one 'Q'."""
    for n in range(1, 7):
        solutions = solve_n_queens(n)
        for sol in solutions:
            assert len(sol) == n
            for row in sol:
                assert len(row) == n
                assert row.count('Q') == 1
                assert set(row) <= {'Q', '.'}


def test_no_conflicts():
    """Verify no two queens share a row, column, or diagonal."""
    for n in range(1, 8):
        solutions = solve_n_queens(n)
        for sol in solutions:
            queen_cols = [row.index('Q') for row in sol]
            for r1 in range(len(queen_cols)):
                for r2 in range(r1 + 1, len(queen_cols)):
                    c1, c2 = queen_cols[r1], queen_cols[r2]
                    assert c1 != c2, "Column conflict"
                    assert abs(r1 - r2) != abs(c1 - c2), "Diagonal conflict"
