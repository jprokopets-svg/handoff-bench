from regex_parser import is_match

# Run the test cases
print("Test 1: is_match('aa', 'a') == False")
result = is_match('aa', 'a')
print(f"Result: {result}, Expected: False, Pass: {result == False}")

print("\nTest 2: is_match('aa', 'a*') == True")
result = is_match('aa', 'a*')
print(f"Result: {result}, Expected: True, Pass: {result == True}")

print("\nTest 3: is_match('ab', '.*') == True")
result = is_match('ab', '.*')
print(f"Result: {result}, Expected: True, Pass: {result == True}")

print("\nTest 4: is_match('aab', 'c*a*b') == True")
result = is_match('aab', 'c*a*b')
print(f"Result: {result}, Expected: True, Pass: {result == True}")

print("\nTest 5: is_match('mississippi', 'mis*is*p*.') == False")
result = is_match('mississippi', 'mis*is*p*.')
print(f"Result: {result}, Expected: False, Pass: {result == False}")

print("\nTest 6: is_match('', '.*') == True")
result = is_match('', '.*')
print(f"Result: {result}, Expected: True, Pass: {result == True}")
