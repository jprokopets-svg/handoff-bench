import pytest
from n_queens import solveNQueens


def test_n_equals_1():
    """Test N-Queens with n=1"""
    result = solveNQueens(1)
    assert len(result) == 1
    assert result[0] == ['Q']


def test_n_equals_4():
    """Test N-Queens with n=4 - should have 2 solutions"""
    result = solveNQueens(4)
    assert len(result) == 2
    
    # Verify each solution is valid
    for solution in result:
        assert len(solution) == 4
        for row in solution:
            assert len(row) == 4
            assert row.count('Q') == 1
            assert all(c in 'Q.' for c in row)


def test_n_equals_8():
    """Test N-Queens with n=8 - should have 92 solutions"""
    result = solveNQueens(8)
    assert len(result) == 92
    
    # Verify each solution is valid
    for solution in result:
        assert len(solution) == 8
        for row in solution:
            assert len(row) == 8
            assert row.count('Q') == 1


def test_solution_format():
    """Test that solutions have the correct format"""
    result = solveNQueens(4)
    
    for solution in result:
        # Each solution should be a list
        assert isinstance(solution, list)
        
        # Each row should be a string
        for row in solution:
            assert isinstance(row, str)
            # Each row should have exactly one queen
            assert row.count('Q') == 1
            # Each row should have the correct length
            assert len(row) == 4


def test_no_conflicts():
    """Test that no two queens attack each other in any solution"""
    result = solveNQueens(4)
    
    for solution in result:
        # Extract queen positions
        queens = []
        for row_idx, row in enumerate(solution):
            for col_idx, cell in enumerate(row):
                if cell == 'Q':
                    queens.append((row_idx, col_idx))
        
        # Check no two queens are in same row, column, or diagonal
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


def test_n_equals_0():
    """Test N-Queens with n=0"""
    result = solveNQueens(0)
    assert len(result) == 1
    assert result[0] == []


def test_n_equals_2():
    """Test N-Queens with n=2 - should have 0 solutions"""
    result = solveNQueens(2)
    assert len(result) == 0


def test_n_equals_3():
    """Test N-Queens with n=3 - should have 0 solutions"""
    result = solveNQueens(3)
    assert len(result) == 0
