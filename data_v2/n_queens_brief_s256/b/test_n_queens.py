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
            assert all(c in ['Q', '.'] for c in row)


def test_n_queens_8():
    """Test N-Queens with n=8"""
    result = solveNQueens(8)
    assert len(result) == 92


def test_n_queens_0():
    """Test N-Queens with n=0"""
    result = solveNQueens(0)
    assert result == []


def test_solution_validity():
    """Test that solutions are valid (no queens attack each other)"""
    result = solveNQueens(4)
    
    for solution in result:
        # Find queen positions
        queens = []
        for row, line in enumerate(solution):
            for col, char in enumerate(line):
                if char == 'Q':
                    queens.append((row, col))
        
        # Check no two queens attack each other
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
