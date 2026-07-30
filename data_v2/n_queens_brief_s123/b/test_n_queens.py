import pytest
from n_queens import solveNQueens


def test_n_queens_n1():
    """Test N-Queens with n=1"""
    result = solveNQueens(1)
    assert len(result) == 1
    assert result[0] == ['Q']


def test_n_queens_n4():
    """Test N-Queens with n=4"""
    result = solveNQueens(4)
    assert len(result) == 2
    
    # Verify each solution is valid
    for solution in result:
        assert len(solution) == 4
        for row in solution:
            assert len(row) == 4
            assert row.count('Q') == 1
        
        # Check no two queens attack each other
        queens = []
        for i, row in enumerate(solution):
            for j, cell in enumerate(row):
                if cell == 'Q':
                    queens.append((i, j))
        
        # Verify no two queens share row, col, or diagonal
        for i in range(len(queens)):
            for j in range(i + 1, len(queens)):
                r1, c1 = queens[i]
                r2, c2 = queens[j]
                assert r1 != r2, "Two queens in same row"
                assert c1 != c2, "Two queens in same column"
                assert abs(r1 - r2) != abs(c1 - c2), "Two queens on same diagonal"


def test_n_queens_n8():
    """Test N-Queens with n=8"""
    result = solveNQueens(8)
    assert len(result) == 92


def test_n_queens_n0():
    """Test N-Queens with n=0"""
    result = solveNQueens(0)
    assert result == []


def test_n_queens_n2():
    """Test N-Queens with n=2 (no solution exists)"""
    result = solveNQueens(2)
    assert len(result) == 0


def test_n_queens_n3():
    """Test N-Queens with n=3 (no solution exists)"""
    result = solveNQueens(3)
    assert len(result) == 0


def test_n_queens_solution_format():
    """Test that solutions have correct format"""
    result = solveNQueens(4)
    for solution in result:
        assert isinstance(solution, list)
        for row in solution:
            assert isinstance(row, str)
            assert all(c in ['Q', '.'] for c in row)
