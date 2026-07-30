from regex_parser import is_match

print('Test 1:', is_match('aa', 'a'), '== False')
print('Test 2:', is_match('aa', 'a*'), '== True')
print('Test 3:', is_match('ab', '.*'), '== True')
print('Test 4:', is_match('aab', 'c*a*b'), '== True')
print('Test 5:', is_match('mississippi', 'mis*is*p*.'), '== False')
print('Test 6:', is_match('', '.*'), '== True')
