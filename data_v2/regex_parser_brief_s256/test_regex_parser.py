from regex_parser import *


assert is_match('aa', 'a') == False

assert is_match('aa', 'a*') == True

assert is_match('ab', '.*') == True

assert is_match('aab', 'c*a*b') == True

assert is_match('mississippi', 'mis*is*p*.') == False

assert is_match('', '.*') == True