from palindromic_substring import *

import pytest


def test_babad():
    assert longest_palindrome('babad') in ('bab', 'aba')

def test_cbbd():
    assert longest_palindrome('cbbd') == 'bb'

def test_single_char():
    assert longest_palindrome('a') == 'a'

def test_no_palindrome():
    assert longest_palindrome('ac') in ('a', 'c')
