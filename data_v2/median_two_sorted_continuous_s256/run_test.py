from median_two_sorted import find_median_sorted_arrays

# Test 1
result1 = find_median_sorted_arrays([1,3], [2])
print(f"Test 1: find_median_sorted_arrays([1,3], [2]) = {result1}, expected 2.0")
assert result1 == 2.0, f"Failed: got {result1}"

# Test 2
result2 = find_median_sorted_arrays([1,2], [3,4])
print(f"Test 2: find_median_sorted_arrays([1,2], [3,4]) = {result2}, expected 2.5")
assert result2 == 2.5, f"Failed: got {result2}"

# Test 3
result3 = find_median_sorted_arrays([0,0], [0,0])
print(f"Test 3: find_median_sorted_arrays([0,0], [0,0]) = {result3}, expected 0.0")
assert result3 == 0.0, f"Failed: got {result3}"

# Test 4
result4 = find_median_sorted_arrays([], [1])
print(f"Test 4: find_median_sorted_arrays([], [1]) = {result4}, expected 1.0")
assert result4 == 1.0, f"Failed: got {result4}"

print("\nAll tests passed!")
