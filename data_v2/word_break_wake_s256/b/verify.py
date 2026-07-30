s = "catsandsanddog"
print(f"String: '{s}'")
print(f"Length: {len(s)}")

# Check possible segmentations
words = ["cat", "cats", "and", "sand", "dog"]

# Try: cats + and + sand + dog
seg1 = "cats" + "and" + "sand" + "dog"
print(f"\n'cats' + 'and' + 'sand' + 'dog' = '{seg1}'")
print(f"Match: {seg1 == s}")

# Try: cat + sand + sand + dog
seg2 = "cat" + "sand" + "sand" + "dog"
print(f"\n'cat' + 'sand' + 'sand' + 'dog' = '{seg2}'")
print(f"Match: {seg2 == s}")

# Try: cat + and + sand + dog
seg3 = "cat" + "and" + "sand" + "dog"
print(f"\n'cat' + 'and' + 'sand' + 'dog' = '{seg3}'")
print(f"Match: {seg3 == s}")

# The actual string character by character
print(f"\nActual string chars: {list(s)}")
print(f"Actual string: {s}")
