from n_queens import solve_n_queens

def test_n1():
    """Test N=1 case"""
    assert solve_n_queens(1) == [["Q"]]

def test_n4_count():
    """Test that N=4 has exactly 2 solutions"""
    assert len(solve_n_queens(4)) == 2

def test_n4_solutions():
    """Test that N=4 solutions are correct"""
    solutions = solve_n_queens(4)
    assert [".Q..", "...Q", "Q...", "..Q."] in solutions
    assert ["..Q.", "Q...", "...Q", ".Q.."] in solutions

def test_n8_count():
    """Test that N=8 has exactly 92 solutions"""
    assert len(solve_n_queens(8)) == 92

def test_solution_format():
    """Test that solutions have correct format"""
    for sol in solve_n_queens(5):
        assert len(sol) == 5
        for row in sol:
            assert len(row) == 5
            assert row.count('Q') == 1
            assert all(c in 'Q.' for c in row)

def test_n2_n3_no_solution():
    """Test that N=2 and N=3 have no solutions"""
    assert solve_n_queens(2) == []
    assert solve_n_queens(3) == []

def test_solution_validity():
    """Test that all solutions are valid (no conflicts)"""
    solutions = solve_n_queens(4)
    for solution in solutions:
        # Check each row has exactly one queen
        for row in solution:
            assert row.count('Q') == 1
        
        # Check no column conflicts
        cols = set()
        for row in solution:
            col = row.index('Q')
            assert col not in cols
            cols.add(col)
        
        # Check no diagonal conflicts
        positions = []
        for i, row in enumerate(solution):
            col = row.index('Q')
            positions.append((i, col))
        
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                r1, c1 = positions[i]
                r2, c2 = positions[j]
                # Check diagonal conflicts
                assert abs(r1 - r2) != abs(c1 - c2)
