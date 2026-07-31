import pytest
from n_queens import solve_n_queens


def test_n1():
    solutions = solve_n_queens(1)
    assert solutions == [['Q']]


def test_n2():
    # No solutions exist for n=2
    solutions = solve_n_queens(2)
    assert solutions == []


def test_n3():
    # No solutions exist for n=3
    solutions = solve_n_queens(3)
    assert solutions == []


def test_n4_count():
    solutions = solve_n_queens(4)
    assert len(solutions) == 2


def test_n4_solutions():
    solutions = solve_n_queens(4)
    expected = [
        ['.Q..', '...Q', 'Q...', '..Q.'],
        ['..Q.', 'Q...', '...Q', '.Q..'],
    ]
    assert sorted(solutions) == sorted(expected)


def test_n5_count():
    solutions = solve_n_queens(5)
    assert len(solutions) == 10


def test_n6_count():
    solutions = solve_n_queens(6)
    assert len(solutions) == 4


def test_n7_count():
    solutions = solve_n_queens(7)
    assert len(solutions) == 40


def test_n8_count():
    solutions = solve_n_queens(8)
    assert len(solutions) == 92


def test_solution_format():
    """Each solution row must be a string of length n with exactly one 'Q'."""
    for n in range(1, 7):
        solutions = solve_n_queens(n)
        for solution in solutions:
            assert len(solution) == n
            for row in solution:
                assert isinstance(row, str)
                assert len(row) == n
                assert row.count('Q') == 1
                assert set(row) <= {'Q', '.'}


def test_no_conflicts():
    """Verify no two queens share a row, column, or diagonal."""
    for n in range(1, 7):
        solutions = solve_n_queens(n)
        for solution in solutions:
            queen_cols = [row.index('Q') for row in solution]
            for r1 in range(len(queen_cols)):
                for r2 in range(r1 + 1, len(queen_cols)):
                    c1, c2 = queen_cols[r1], queen_cols[r2]
                    # No same column
                    assert c1 != c2
                    # No same diagonal
                    assert abs(r1 - r2) != abs(c1 - c2)


def test_n0():
    """n=0 edge case: one empty solution."""
    solutions = solve_n_queens(0)
    assert solutions == [[]]
