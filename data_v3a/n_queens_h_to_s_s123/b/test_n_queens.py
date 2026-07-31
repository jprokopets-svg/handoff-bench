import pytest
from n_queens import solveNQueens


def test_n1():
    result = solveNQueens(1)
    assert result == [["Q"]]


def test_n2():
    result = solveNQueens(2)
    assert result == []


def test_n3():
    result = solveNQueens(3)
    assert result == []


def test_n4():
    result = solveNQueens(4)
    assert len(result) == 2
    # Verify format: each solution is a list of 4 strings, each of length 4
    for solution in result:
        assert len(solution) == 4
        for row in solution:
            assert len(row) == 4
            assert row.count('Q') == 1
            assert set(row) <= {'Q', '.'}


def test_n4_solutions():
    result = solveNQueens(4)
    expected = [
        [".Q..", "...Q", "Q...", "..Q."],
        ["..Q.", "Q...", "...Q", ".Q.."],
    ]
    # Sort both for comparison
    result_sorted = sorted(result)
    expected_sorted = sorted(expected)
    assert result_sorted == expected_sorted


def test_n5():
    result = solveNQueens(5)
    assert len(result) == 10


def test_n6():
    result = solveNQueens(6)
    assert len(result) == 4


def test_n8():
    result = solveNQueens(8)
    assert len(result) == 92


def test_format():
    """Verify that each solution has correct format."""
    for n in range(1, 7):
        result = solveNQueens(n)
        for solution in result:
            assert len(solution) == n
            for row in solution:
                assert isinstance(row, str)
                assert len(row) == n
                assert row.count('Q') == 1


def test_no_attacking_queens():
    """Verify that no two queens attack each other in any solution."""
    for n in range(1, 7):
        result = solveNQueens(n)
        for solution in result:
            queen_positions = []
            for r, row in enumerate(solution):
                c = row.index('Q')
                queen_positions.append((r, c))
            # Check all pairs
            for i in range(len(queen_positions)):
                for j in range(i + 1, len(queen_positions)):
                    r1, c1 = queen_positions[i]
                    r2, c2 = queen_positions[j]
                    # Same column
                    assert c1 != c2
                    # Same diagonal
                    assert abs(r1 - r2) != abs(c1 - c2)
