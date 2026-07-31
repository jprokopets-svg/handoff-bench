import pytest
from regex_parser import is_match


# Basic literal matching
def test_exact_match():
    assert is_match("abc", "abc") is True

def test_no_match():
    assert is_match("abc", "abd") is False

def test_empty_string_empty_pattern():
    assert is_match("", "") is True

def test_empty_string_nonempty_pattern():
    assert is_match("", "a") is False

def test_nonempty_string_empty_pattern():
    assert is_match("a", "") is False


# Dot '.' matching
def test_dot_matches_any_char():
    assert is_match("a", ".") is True

def test_dot_matches_any_char2():
    assert is_match("z", ".") is True

def test_dot_does_not_match_empty():
    assert is_match("", ".") is False

def test_dot_in_middle():
    assert is_match("abc", "a.c") is True

def test_dot_mismatch_length():
    assert is_match("ab", "a.c") is False

def test_all_dots():
    assert is_match("xyz", "...") is True


# Star '*' matching
def test_star_zero_occurrences():
    assert is_match("b", "a*b") is True

def test_star_one_occurrence():
    assert is_match("ab", "a*b") is True

def test_star_multiple_occurrences():
    assert is_match("aaab", "a*b") is True

def test_star_empty_string():
    assert is_match("", "a*") is True

def test_star_only():
    assert is_match("aaa", "a*") is True

def test_star_no_match():
    assert is_match("b", "a*c") is False

def test_star_with_dot():
    assert is_match("anything", ".*") is True

def test_star_with_dot_empty():
    assert is_match("", ".*") is True


# Complex patterns
def test_complex_pattern_1():
    assert is_match("aab", "c*a*b") is True

def test_complex_pattern_2():
    assert is_match("mississippi", "mis*is*p*.") is False

def test_complex_pattern_3():
    assert is_match("mississippi", "mis*is*ip*.") is True

def test_multiple_stars():
    assert is_match("aabbc", "a*b*c") is True

def test_multiple_stars_zero():
    assert is_match("c", "a*b*c") is True

def test_dot_star_middle():
    assert is_match("abcdef", "a.*f") is True

def test_dot_star_no_match():
    assert is_match("abcdef", "a.*z") is False

def test_repeated_pattern():
    assert is_match("aaaa", "a*a") is True

def test_pattern_longer_than_string():
    assert is_match("a", "ab*") is True

def test_full_wildcard():
    assert is_match("hello world", ".*") is True
