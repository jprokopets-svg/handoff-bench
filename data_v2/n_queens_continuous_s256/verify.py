from n_queens import solve_n_queens

# Quick verification
result = solve_n_queens(4)
print(f"Number of solutions for 4-queens: {len(result)}")
print(f"Expected: 2")
print()

for i, sol in enumerate(result, 1):
    print(f"Solution {i}:")
    for row in sol:
        print(row)
    print()

result_1 = solve_n_queens(1)
print(f"Number of solutions for 1-queens: {len(result_1)}")
print(f"Expected: 1")
for row in result_1[0]:
    print(row)
