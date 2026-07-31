import pytest
from n_queens import solveNQueens


def is_valid_solution(solution, n):
    """Helper to validate a single N-Queens solution."""
    assert len(solution) == n, f"Solution should have {n} rows"
    
    queens = []
    for row_idx, row in enumerate(solution):
        assert len(row) == n, f"Each row should have {n} characters"
        assert row.count('Q') == 1, f"Each row should have exactly one queen"
        col_idx = row.index('Q')
        queens.append((row_idx, col_idx))
    
    # Check no two queens attack each other
    for i in range(len(queens)):
        for j in range(i + 1, len(queens)):
            r1, c1 = queens[i]
            r2, c2 = queens[j]
            assert c1 != c2, "Two queens in the same column"
            assert abs(r1 - r2) != abs(c1 - c2), "Two queens on the same diagonal"
    
    return True


def test_n1():
    """n=1 should return exactly one solution: a single queen."""
    result = solveNQueens(1)
    assert len(result) == 1
    assert result[0] == ['Q']


def test_n2():
    """n=2 has no solutions."""
    result = solveNQueens(2)
    assert len(result) == 0


def test_n3():
    """n=3 has no solutions."""
    result = solveNQueens(3)
    assert len(result) == 0


def test_n4():
    """n=4 should return exactly 2 solutions."""
    result = solveNQueens(4)
    assert len(result) == 2
    for solution in result:
        is_valid_solution(solution, 4)


def test_n4_solutions():
    """Verify the actual content of n=4 solutions."""
    result = solveNQueens(4)
    expected = [
        [".Q..", "...Q", "Q...", "..Q."],
        ["..Q.", "Q...", "...Q", ".Q.."]
    ]
    # Sort both for comparison since order may vary
    result_sorted = sorted([tuple(s) for s in result])
    expected_sorted = sorted([tuple(s) for s in expected])
    assert result_sorted == expected_sorted


def test_n5():
    """n=5 should return exactly 10 solutions."""
    result = solveNQueens(5)
    assert len(result) == 10
    for solution in result:
        is_valid_solution(solution, 5)


def test_n6():
    """n=6 should return exactly 4 solutions."""
    result = solveNQueens(6)
    assert len(result) == 4
    for solution in result:
        is_valid_solution(solution, 6)


def test_n7():
    """n=7 should return exactly 40 solutions."""
    result = solveNQueens(7)
    assert len(result) == 40
    for solution in result:
        is_valid_solution(solution, 7)


def test_n8():
    """n=8 (classic problem) should return exactly 92 solutions."""
    result = solveNQueens(8)
    assert len(result) == 92
    for solution in result:
        is_valid_solution(solution, 8)


def test_all_solutions_valid():
    """All solutions for n=4 through n=8 should be valid."""
    for n in range(4, 9):
        result = solveNQueens(n)
        for solution in result:
            is_valid_solution(solution, n)


def test_return_type():
    """Result should be a list of lists of strings."""
    result = solveNQueens(4)
    assert isinstance(result, list)
    for solution in result:
        assert isinstance(solution, list)
        for row in solution:
            assert isinstance(row, str)


def test_no_duplicate_solutions():
    """There should be no duplicate solutions."""
    for n in [4, 5, 6]:
        result = solveNQueens(n)
        unique = set(tuple(tuple(row) for row in sol) for sol in result)
        assert len(unique) == len(result), f"Duplicate solutions found for n={n}"
