from regex_matcher import *


def _raises(fn):
    try:
        fn()
        return False
    except ValueError:
        return True

assert full_match('abc', 'abc') == True

assert full_match('abc', 'abd') == False

assert full_match('a.c', 'abc') == True

assert full_match('a.c', 'ac') == False

assert full_match('ab*c', 'ac') == True

assert full_match('ab*c', 'abbbc') == True

assert full_match('ab*c', 'abbd') == False

assert full_match('ab+c', 'abc') == True

assert full_match('ab+c', 'ac') == False

assert full_match('colou?r', 'color') == True

assert full_match('colou?r', 'colour') == True

assert full_match('[a-c]x', 'bx') == True

assert full_match('[a-c]x', 'dx') == False

assert full_match('[^0-9]', 'a') == True

assert full_match('[^0-9]', '5') == False

assert full_match('(ab|cd)e', 'abe') == True

assert full_match('(ab|cd)e', 'cde') == True

assert full_match('(ab|cd)e', 'ade') == False

assert full_match('(a(b|c))', 'ab') == True

assert full_match('^abc$', 'abc') == True

assert full_match('^abc$', 'abcd') == False

assert full_match('^a', 'a') == True

assert full_match('a$', 'ba') == False

assert full_match('a\\.b', 'a.b') == True

assert full_match('a\\.b', 'axb') == False

assert full_match('\\*', '*') == True

assert full_match('(ab)*', 'abab') == True

assert full_match('(ab)*', 'aba') == False

assert full_match('a*ab', 'aaab') == True

assert _raises(lambda: full_match('(ab', 'x'))

assert _raises(lambda: full_match('*a', 'x'))

assert _raises(lambda: full_match('[ab', 'x'))