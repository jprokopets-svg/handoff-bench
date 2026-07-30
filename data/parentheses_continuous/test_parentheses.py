from parentheses import *

import pytest


assert sorted(generate_parentheses(1)) == sorted(['()'])

assert sorted(generate_parentheses(2)) == sorted(['()()', '(())'])

assert len(generate_parentheses(3)) == 5

assert sorted(generate_parentheses(3)) == sorted(['((()))','(()())','(())()','()(())','()()()'])