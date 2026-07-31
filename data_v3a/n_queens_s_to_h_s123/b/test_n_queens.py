import pytest
from n_queens import solve_n_queens


def test_n1():
    """Test n=1: should have 1 solution"""
    result = solve_n_queens(1)
    assert len(result) == 1
    assert result == [["Q"]]


def test_n2():
    """Test n=2: should have 0 solutions"""
    result = solve_n_queens(2)
    assert result == []


def test_n3():
    """Test n=3: should have 0 solutions"""
    result = solve_n_queens(3)
    assert result == []


def test_n4():
    """Test n=4: should have 2 solutions"""
    result = solve_n_queens(4)
    assert len(result) == 2
    
    # Verify each solution is valid
    for solution in result:
        assert len(solution) == 4
        for row in solution:
            assert len(row) == 4
            assert row.count('Q') == 1


def test_n8():
    """Test n=8: should have 92 solutions"""
    result = solve_n_queens(8)
    assert len(result) == 92


def test_solution_validity_n4():
    """Verify that n=4 solutions are actually valid"""
    result = solve_n_queens(4)
    
    for solution in result:
        # Check each row has exactly one queen
        for row in solution:
            assert row.count('Q') == 1
        
        # Check each column has exactly one queen
        for col in range(4):
            queen_count = sum(1 for row in solution if row[col] == 'Q')
            assert queen_count == 1
        
        # Check diagonals
        queen_positions = []
        for row_idx, row in enumerate(solution):
            for col_idx, cell in enumerate(row):
                if cell == 'Q':
                    queen_positions.append((row_idx, col_idx))
        
        # Check no two queens on same diagonal
        for i in range(len(queen_positions)):
            for j in range(i + 1, len(queen_positions)):
                r1, c1 = queen_positions[i]
                r2, c2 = queen_positions[j]
                # Not on same diagonal if abs(r1-r2) != abs(c1-c2)
                assert abs(r1 - r2) != abs(c1 - c2)
