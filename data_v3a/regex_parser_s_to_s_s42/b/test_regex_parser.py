import pytest
from regex_parser import is_match

def test_exact_match():
    assert is_match("abc", "abc") == True

def test_no_match():
    assert is_match("abc", "abd") == False

def test_dot_matches_any_char():
    assert is_match("abc", "a.c") == True

def test_dot_matches_any_single():
    assert is_match("aXc", "a.c") == True

def test_star_zero_occurrences():
    assert is_match("ac", "ab*c") == True

def test_star_one_occurrence():
    assert is_match("abc", "ab*c") == True

def test_star_multiple_occurrences():
    assert is_match("abbbbc", "ab*c") == True

def test_dot_star_matches_anything():
    assert is_match("anything", ".*") == True

def test_dot_star_matches_empty():
    assert is_match("", ".*") == True

def test_empty_string_empty_pattern():
    assert is_match("", "") == True

def test_empty_string_nonempty_pattern():
    assert is_match("", "a") == False

def test_nonempty_string_empty_pattern():
    assert is_match("a", "") == False

def test_star_eliminates_preceding():
    assert is_match("aaa", "a*") == True

def test_star_zero_with_dot():
    assert is_match("b", "a*b") == True

def test_complex_pattern():
    assert is_match("aab", "c*a*b") == True

def test_complex_no_match():
    assert is_match("mississippi", "mis*is*p*.") == False

def test_single_dot():
    assert is_match("a", ".") == True

def test_dot_no_match_empty():
    assert is_match("", ".") == False

def test_repeated_pattern():
    assert is_match("aaaa", "a*a") == True

def test_star_with_dot_multiple():
    assert is_match("abcdef", ".*") == True
