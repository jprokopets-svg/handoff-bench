from regex_parser import *


def test_basic():
    assert is_match('aa', 'a') == False

def test_star():
    assert is_match('aa', 'a*') == True

def test_dot_star():
    assert is_match('ab', '.*') == True

def test_complex_pattern():
    assert is_match('aab', 'c*a*b') == True

def test_mississippi():
    assert is_match('mississippi', 'mis*is*p*.') == False

def test_empty_string():
    assert is_match('', '.*') == True
