from text_justification import *


assert full_justify(['This', 'is', 'an', 'example', 'of', 'text', 'justification.'], 16) == ['This    is    an', 'example  of text', 'justification.  ']

assert full_justify(['This', 'is', 'an', 'example', 'of', 'text', 'justification.'], 15) == ['This    is   an', 'example of text', 'justification. ']

assert full_justify(['hello'], 10) == ['hello     ']

assert full_justify(['a', 'b', 'c'], 3) == ['a b', 'c  ']

assert full_justify(['ab', 'cd'], 5) == ['ab cd']

assert full_justify(['a', 'b', 'c', 'd'], 7) == ['a b c d']

assert full_justify(['What', 'must', 'be', 'acknowledgment', 'shall', 'be'], 16) == ['What   must   be', 'acknowledgment  ', 'shall be        ']

assert full_justify(['Science', 'is', 'what', 'we', 'understand', 'well', 'enough', 'to', 'explain', 'to', 'a', 'computer.', 'Art', 'is', 'everything', 'else', 'we', 'do'], 20) == ['Science  is  what we', 'understand      well', 'enough to explain to', 'a  computer.  Art is', 'everything  else  we', 'do                  ']