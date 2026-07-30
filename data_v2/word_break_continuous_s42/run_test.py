from word_break import word_break

# Test 1
result1 = word_break('leetcode', ['leet','code'])
print(f"Test 1: word_break('leetcode', ['leet','code']) = {result1}, expected True")
assert result1 == True, f"Test 1 failed: got {result1}"

# Test 2
result2 = word_break('applepenapple', ['apple','pen'])
print(f"Test 2: word_break('applepenapple', ['apple','pen']) = {result2}, expected True")
assert result2 == True, f"Test 2 failed: got {result2}"

# Test 3
result3 = word_break('catsandog', ['cats','dog','sand','and','cat'])
print(f"Test 3: word_break('catsandog', ['cats','dog','sand','and','cat']) = {result3}, expected False")
assert result3 == False, f"Test 3 failed: got {result3}"

# Test 4
result4 = word_break('', ['a'])
print(f"Test 4: word_break('', ['a']) = {result4}, expected True")
assert result4 == True, f"Test 4 failed: got {result4}"

print("\nAll tests passed!")
