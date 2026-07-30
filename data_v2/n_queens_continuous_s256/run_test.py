from n_queens import solve_n_queens

# Test 1: 4-queens should have 2 solutions
result_4 = solve_n_queens(4)
print(f"4-queens solutions: {len(result_4)}")
assert len(result_4) == 2, f"Expected 2 solutions for 4-queens, got {len(result_4)}"
print("✓ Test 1 passed: 4-queens has 2 solutions")

# Test 2: 1-queen should have 1 solution
result_1 = solve_n_queens(1)
print(f"1-queens solutions: {len(result_1)}")
assert len(result_1) == 1, f"Expected 1 solution for 1-queens, got {len(result_1)}"
print("✓ Test 2 passed: 1-queens has 1 solution")

# Test 3: Each row should have length 4
assert all(len(row) == 4 for sol in solve_n_queens(4) for row in sol), "Not all rows have length 4"
print("✓ Test 3 passed: All rows have correct length")

# Test 4: Each row should have exactly 1 queen
assert all(row.count('Q') == 1 for sol in solve_n_queens(4) for row in sol), "Not all rows have exactly 1 queen"
print("✓ Test 4 passed: All rows have exactly 1 queen")

print("\nAll tests passed!")
print("\n4-Queens solutions:")
for i, sol in enumerate(result_4, 1):
    print(f"Solution {i}:")
    for row in sol:
        print(row)
    print()
