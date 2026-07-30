from median_stream import MedianFinder

# Test 1
mf = MedianFinder()
mf.add_num(1)
mf.add_num(2)
result = mf.find_median()
print(f"Test 1: {result} == 1.5? {result == 1.5}")
assert result == 1.5, f"Expected 1.5, got {result}"

# Test 2
mf = MedianFinder()
mf.add_num(1)
result = mf.find_median()
print(f"Test 2: {result} == 1.0? {result == 1.0}")
assert result == 1.0, f"Expected 1.0, got {result}"

# Test 3
mf = MedianFinder()
mf.add_num(1)
mf.add_num(2)
mf.add_num(3)
result = mf.find_median()
print(f"Test 3: {result} == 2.0? {result == 2.0}")
assert result == 2.0, f"Expected 2.0, got {result}"

print("\nAll tests passed!")
