import pytest
from n_queens import solveNQueens


def test_n_queens_n1():
    """Test N-Queens with n=1"""
    result = solveNQueens(1)
    assert len(result) == 1
    assert result[0] == ['Q']


def test_n_queens_n4():
    """Test N-Queens with n=4 (should have 2 solutions)"""
    result = solveNQueens(4)
    assert len(result) == 2
    
    # Verify each solution has 4 rows
    for solution in result:
        assert len(solution) == 4
        # Verify each row has exactly one Q
        for row in solution:
            assert row.count('Q') == 1
            assert len(row) == 4


def test_n_queens_n8():
    """Test N-Queens with n=8 (should have 92 solutions)"""
    result = solveNQueens(8)
    assert len(result) == 92


def test_n_queens_n0():
    """Test N-Queens with n=0"""
    result = solveNQueens(0)
    assert len(result) == 1
    assert result[0] == []


def test_n_queens_format():
    """Test that solutions are properly formatted"""
    result = solveNQueens(4)
    for solution in result:
        for row in solution:
            # Each row should be a string
            assert isinstance(row, str)
            # Each row should have exactly one Q
            assert row.count('Q') == 1
            # Each row should have n characters
            assert len(row) == 4
            # Each character should be Q or .
            assert all(c in ['Q', '.'] for c in row)


def test_n_queens_valid_placement():
    """Test that queens don't attack each other"""
    result = solveNQueens(4)
    
    for solution in result:
        # Extract queen positions
        queen_positions = []
        for row, line in enumerate(solution):
            col = line.index('Q')
            queen_positions.append((row, col))
        
        # Check no two queens are in same row, column, or diagonal
        for i in range(len(queen_positions)):
            for j in range(i + 1, len(queen_positions)):
                r1, c1 = queen_positions[i]
                r2, c2 = queen_positions[j]
                
                # Different rows (guaranteed by construction)
                assert r1 != r2
                # Different columns
                assert c1 != c2
                # Different diagonals
                assert abs(r1 - r2) != abs(c1 - c2)
