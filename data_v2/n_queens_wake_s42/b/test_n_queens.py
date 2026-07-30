import pytest
from n_queens import solveNQueens


def test_n_queens_1():
    """Test N-Queens with n=1"""
    result = solveNQueens(1)
    assert len(result) == 1
    assert result[0] == ['Q']


def test_n_queens_4():
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
        
        # Verify all queens are on different rows, columns, and diagonals
        for i, (r1, c1) in enumerate(queens):
            for r2, c2 in queens[i+1:]:
                assert r1 != r2, "Queens on same row"
                assert c1 != c2, "Queens on same column"
                assert abs(r1 - r2) != abs(c1 - c2), "Queens on same diagonal"


def test_n_queens_0():
    """Test N-Queens with n=0"""
    result = solveNQueens(0)
    assert result == []


def test_n_queens_8():
    """Test N-Queens with n=8"""
    result = solveNQueens(8)
    assert len(result) == 92
    
    # Verify each solution is valid
    for solution in result:
        assert len(solution) == 8
        for row in solution:
            assert len(row) == 8
            assert row.count('Q') == 1


def test_n_queens_format():
    """Test that output format is correct"""
    result = solveNQueens(2)
    # n=2 has no solutions
    assert result == []
    
    result = solveNQueens(3)
    # n=3 has no solutions
    assert result == []
