import pytest
from n_queens import solve_n_queens


def test_n1():
    result = solve_n_queens(1)
    assert result == [["Q"]]


def test_n2():
    result = solve_n_queens(2)
    assert result == []


def test_n3():
    result = solve_n_queens(3)
    assert result == []


def test_n4():
    result = solve_n_queens(4)
    assert len(result) == 2
    expected = [
        [".Q..", "...Q", "Q...", "..Q."],
        ["..Q.", "Q...", "...Q", ".Q.."]
    ]
    assert sorted(result) == sorted(expected)


def test_n5():
    result = solve_n_queens(5)
    assert len(result) == 10


def test_n6():
    result = solve_n_queens(6)
    assert len(result) == 4


def test_n7():
    result = solve_n_queens(7)
    assert len(result) == 40


def test_n8():
    result = solve_n_queens(8)
    assert len(result) == 92


def test_board_format():
    """Each row must have exactly one 'Q' and the rest '.'"""
    for solution in solve_n_queens(5):
        assert len(solution) == 5
        for row in solution:
            assert len(row) == 5
            assert row.count('Q') == 1
            assert row.count('.') == 4


def test_no_conflicts():
    """Verify no two queens share a row, column, or diagonal."""
    for solution in solve_n_queens(6):
        positions = []
        for r, row in enumerate(solution):
            c = row.index('Q')
            positions.append((r, c))
        cols = [c for r, c in positions]
        assert len(set(cols)) == len(cols), "Column conflict"
        diag1 = [r - c for r, c in positions]
        assert len(set(diag1)) == len(diag1), "Diagonal conflict"
        diag2 = [r + c for r, c in positions]
        assert len(set(diag2)) == len(diag2), "Anti-diagonal conflict"
