from parentheses import generate_parentheses

# Test 1
result1 = sorted(generate_parentheses(1))
expected1 = sorted(['()'])
print(f"Test 1: {result1 == expected1}")
print(f"  Result: {result1}")
print(f"  Expected: {expected1}")

# Test 2
result2 = sorted(generate_parentheses(2))
expected2 = sorted(['()()', '(())'])
print(f"Test 2: {result2 == expected2}")
print(f"  Result: {result2}")
print(f"  Expected: {expected2}")

# Test 3
result3 = len(generate_parentheses(3))
expected3 = 5
print(f"Test 3: {result3 == expected3}")
print(f"  Result length: {result3}")
print(f"  Expected length: {expected3}")

# Test 4
result4 = sorted(generate_parentheses(3))
expected4 = sorted(['((()))','(()())','(())()','()(())','()()()'])
print(f"Test 4: {result4 == expected4}")
print(f"  Result: {result4}")
print(f"  Expected: {expected4}")
