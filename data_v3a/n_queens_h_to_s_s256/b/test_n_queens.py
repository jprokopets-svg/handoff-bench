import pytest
from n_queens import solveNQueens


def test_n_equals_1():
    solutions = solveNQueens(1)
    assert solutions == [['Q']]


def test_n_equals_2():
    solutions = solveNQueens(2)
    assert solutions == []


def test_n_equals_3():
    solutions = solveNQueens(3)
    assert solutions == []


def test_n_equals_4():
    solutions = solveNQueens(4)
    assert len(solutions) == 2
    # Verify each solution is valid
    for sol in solutions:
        assert len(sol) == 4
        for row in sol:
            assert len(row) == 4
            assert row.count('Q') == 1
    # Check the two known solutions
    expected = [
        [".Q..", "...Q", "Q...", "..Q."],
        ["..Q.", "Q...", "...Q", ".Q.."]
    ]
    for e in expected:
        assert e in solutions


def test_n_equals_5():
    solutions = solveNQueens(5)
    assert len(solutions) == 10


def test_n_equals_6():
    solutions = solveNQueens(6)
    assert len(solutions) == 4


def test_n_equals_7():
    solutions = solveNQueens(7)
    assert len(solutions) == 40


def test_n_equals_8():
    solutions = solveNQueens(8)
    assert len(solutions) == 92


def test_solutions_are_valid():
    """Verify that all solutions for n=6 have non-attacking queens."""
    n = 6
    solutions = solveNQueens(n)
    for sol in solutions:
        # Find queen positions
        queens = []
        for r, row in enumerate(sol):
            c = row.index('Q')
            queens.append((r, c))
        # Check no two queens attack each other
        for i in range(len(queens)):
            for j in range(i + 1, len(queens)):
                r1, c1 = queens[i]
                r2, c2 = queens[j]
                assert c1 != c2, "Two queens in same column"
                assert r1 != r2, "Two queens in same row"
                assert abs(r1 - r2) != abs(c1 - c2), "Two queens on same diagonal"


def test_solution_format():
    """Verify the format of solutions."""
    solutions = solveNQueens(4)
    for sol in solutions:
        assert isinstance(sol, list)
        for row in sol:
            assert isinstance(row, str)
            assert set(row).issubset({'.', 'Q'})
            assert row.count('Q') == 1
