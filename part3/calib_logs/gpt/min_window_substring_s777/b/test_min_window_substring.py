from min_window_substring import *


assert min_window('ADOBECODEBANC', 'ABC') == 'BANC'

assert min_window('a', 'a') == 'a'

assert min_window('a', 'aa') == ''

assert min_window('ab', 'a') == 'a'

assert min_window('cabwefgewcwaefgcf', 'cae') == 'cwae'