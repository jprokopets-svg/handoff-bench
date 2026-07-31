import pytest
from n_queens import solveNQueens


def is_valid_solution(board, n):
    """Helper function to validate a solution."""
    # Check that there are exactly n queens
    queen_count = sum(row.count('Q') for row in board)
    if queen_count != n:
        return False
    
    # Check that each row has exactly one queen
    for row in board:
        if row.count('Q') != 1:
            return False
    
    # Check that each column has exactly one queen
    for col in range(n):
        col_count = sum(1 for row in range(n) if board[row][col] == 'Q')
        if col_count != 1:
            return False
    
    # Check diagonals - no two queens attack each other
    queen_positions = []
    for row in range(n):
        for col in range(n):
            if board[row][col] == 'Q':
                queen_positions.append((row, col))
    
    for i, (r1, c1) in enumerate(queen_positions):
        for r2, c2 in queen_positions[i+1:]:
            # Check if on same diagonal
            if abs(r1 - r2) == abs(c1 - c2):
                return False
    
    return True


def test_n_queens_n1():
    """Test N-Queens with n=1."""
    result = solveNQueens(1)
    assert len(result) == 1
    assert result[0] == ['Q']
    assert is_valid_solution(result[0], 1)


def test_n_queens_n4():
    """Test N-Queens with n=4."""
    result = solveNQueens(4)
    assert len(result) == 2
    for solution in result:
        assert len(solution) == 4
        assert is_valid_solution(solution, 4)


def test_n_queens_n8():
    """Test N-Queens with n=8."""
    result = solveNQueens(8)
    assert len(result) == 92
    for solution in result:
        assert len(solution) == 8
        assert is_valid_solution(solution, 8)


def test_n_queens_n0():
    """Test N-Queens with n=0 (edge case)."""
    result = solveNQueens(0)
    # For n=0, we should return one empty solution
    assert len(result) == 1
    assert result[0] == []


def test_n_queens_n2():
    """Test N-Queens with n=2 (impossible case)."""
    result = solveNQueens(2)
    assert len(result) == 0


def test_n_queens_n3():
    """Test N-Queens with n=3 (impossible case)."""
    result = solveNQueens(3)
    assert len(result) == 0


def test_n_queens_format():
    """Test that solutions are in the correct format."""
    result = solveNQueens(4)
    for solution in result:
        assert isinstance(solution, list)
        for row in solution:
            assert isinstance(row, str)
            assert all(c in ['Q', '.'] for c in row)
