import pytest
from n_queens import solveNQueens


def test_n_queens_n1():
    """Test N-Queens with n=1"""
    result = solveNQueens(1)
    assert len(result) == 1
    assert result[0] == ['Q']


def test_n_queens_n2():
    """Test N-Queens with n=2 - no solutions exist"""
    result = solveNQueens(2)
    assert len(result) == 0


def test_n_queens_n3():
    """Test N-Queens with n=3 - no solutions exist"""
    result = solveNQueens(3)
    assert len(result) == 0


def test_n_queens_n4():
    """Test N-Queens with n=4 - exactly 2 solutions"""
    result = solveNQueens(4)
    assert len(result) == 2
    
    # Verify each solution is valid
    for solution in result:
        assert len(solution) == 4
        for row in solution:
            assert len(row) == 4
            assert row.count('Q') == 1
            assert all(c in 'Q.' for c in row)


def test_n_queens_n8():
    """Test N-Queens with n=8 - exactly 92 solutions"""
    result = solveNQueens(8)
    assert len(result) == 92
    
    # Verify each solution is valid
    for solution in result:
        assert len(solution) == 8
        for row in solution:
            assert len(row) == 8
            assert row.count('Q') == 1


def test_n_queens_solution_validity():
    """Test that solutions are actually valid (no queens attack each other)"""
    result = solveNQueens(4)
    
    for solution in result:
        # Extract queen positions
        queens = []
        for row, line in enumerate(solution):
            col = line.index('Q')
            queens.append((row, col))
        
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


def test_n_queens_format():
    """Test that output format is correct"""
    result = solveNQueens(4)
    
    for solution in result:
        # Should be a list of strings
        assert isinstance(solution, list)
        assert all(isinstance(row, str) for row in solution)
        
        # Each row should have exactly one Q
        for row in solution:
            assert row.count('Q') == 1
            assert row.count('.') == 3
