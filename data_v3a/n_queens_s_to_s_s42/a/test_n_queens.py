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
    """Each board row must be a string of length n with exactly one 'Q'."""
    for n in range(1, 7):
        solutions = solve_n_queens(n)
        for board in solutions:
            assert len(board) == n
            for row in board:
                assert isinstance(row, str)
                assert len(row) == n
                assert row.count('Q') == 1
                assert set(row) <= {'Q', '.'}


def test_no_conflicts():
    """No two queens should attack each other."""
    for n in range(1, 7):
        solutions = solve_n_queens(n)
        for board in solutions:
            queens = []
            for r, row in enumerate(board):
                c = row.index('Q')
                queens.append((r, c))
            for i in range(len(queens)):
                for j in range(i + 1, len(queens)):
                    r1, c1 = queens[i]
                    r2, c2 = queens[j]
                    assert c1 != c2, "Column conflict"
                    assert abs(r1 - r2) != abs(c1 - c2), "Diagonal conflict"


def test_distinct_solutions():
    """All solutions should be distinct."""
    for n in range(1, 8):
        solutions = solve_n_queens(n)
        tuples = [tuple(board) for board in solutions]
        assert len(tuples) == len(set(tuples)), f"Duplicate solutions for n={n}"
