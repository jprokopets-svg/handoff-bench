from palindromic_substring import longest_palindrome
import pytest


def test_babad():
    assert longest_palindrome('babad') in ('bab', 'aba')


def test_cbbd():
    assert longest_palindrome('cbbd') == 'bb'


def test_single_char():
    assert longest_palindrome('a') == 'a'


def test_two_chars():
    assert longest_palindrome('ac') in ('a', 'c')
