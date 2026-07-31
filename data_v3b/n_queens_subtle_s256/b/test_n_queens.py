import pytest
from n_queens import solveNQueens


def test_n_queens_1():
    """Test N-Queens with n=1"""
    result = solveNQueens(1)
    assert len(result) == 1
    assert result[0] == ['Q']


def test_n_queens_2():
    """Test N-Queens with n=2 - no solution exists"""
    result = solveNQueens(2)
    assert len(result) == 0


def test_n_queens_3():
    """Test N-Queens with n=3 - no solution exists"""
    result = solveNQueens(3)
    assert len(result) == 0


def test_n_queens_4():
    """Test N-Queens with n=4 - 2 solutions"""
    result = solveNQueens(4)
    assert len(result) == 2
    # Verify each solution is valid
    for solution in result:
        assert len(solution) == 4
        for row in solution:
            assert len(row) == 4
            assert row.count('Q') == 1


def test_n_queens_5():
    """Test N-Queens with n=5 - 10 solutions"""
    result = solveNQueens(5)
    assert len(result) == 10


def test_n_queens_8():
    """Test N-Queens with n=8 - 92 solutions"""
    result = solveNQueens(8)
    assert len(result) == 92


def test_solution_format():
    """Test that solutions have correct format"""
    result = solveNQueens(4)
    for solution in result:
        # Each solution should be a list of strings
        assert isinstance(solution, list)
        assert len(solution) == 4
        for row in solution:
            assert isinstance(row, str)
            assert len(row) == 4
            # Each row should have exactly one queen
            assert row.count('Q') == 1
            # Rest should be dots
            assert row.count('.') == 3


def test_no_queen_attacks():
    """Test that no queens attack each other in solutions"""
    result = solveNQueens(4)
    for solution in result:
        # Extract queen positions
        queens = []
        for row_idx, row in enumerate(solution):
            for col_idx, cell in enumerate(row):
                if cell == 'Q':
                    queens.append((row_idx, col_idx))
        
        # Check no two queens are on same row, column, or diagonal
        for i in range(len(queens)):
            for j in range(i + 1, len(queens)):
                r1, c1 = queens[i]
                r2, c2 = queens[j]
                # Different rows (guaranteed by construction)
                assert r1 != r2
                # Different columns
                assert c1 != c2
                # Different diagonals
                assert abs(r1 - r2) != abs(c1 - c2)
