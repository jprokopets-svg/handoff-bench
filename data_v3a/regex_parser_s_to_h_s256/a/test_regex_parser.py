import pytest
from regex_parser import is_match


# Basic literal matching
def test_exact_match():
    assert is_match("abc", "abc") is True

def test_no_match_different_chars():
    assert is_match("abc", "abd") is False

def test_no_match_different_length():
    assert is_match("ab", "abc") is False

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

def test_multiple_dots():
    assert is_match("abc", "...") is True

def test_dot_in_middle():
    assert is_match("abc", "a.c") is True

def test_dot_mismatch_length():
    assert is_match("ab", "a.c") is False


# Star '*' matching
def test_star_zero_occurrences():
    assert is_match("", "a*") is True

def test_star_one_occurrence():
    assert is_match("a", "a*") is True

def test_star_multiple_occurrences():
    assert is_match("aaa", "a*") is True

def test_star_mismatch():
    assert is_match("b", "a*") is False

def test_star_with_prefix():
    assert is_match("aab", "a*b") is True

def test_star_zero_then_literal():
    assert is_match("b", "a*b") is True

def test_star_with_dot():
    assert is_match("abc", ".*") is True

def test_star_with_dot_empty():
    assert is_match("", ".*") is True

def test_star_eliminates_preceding():
    assert is_match("aab", "c*a*b") is True


# Combined patterns
def test_combined_dot_star():
    assert is_match("mississippi", "mis*is*p*.") is False

def test_combined_2():
    assert is_match("aa", "a") is False

def test_combined_3():
    assert is_match("aa", "a*") is True

def test_combined_4():
    assert is_match("ab", ".*") is True

def test_combined_5():
    assert is_match("aab", "c*a*b") is True

def test_combined_6():
    assert is_match("mississippi", "mis*is*ip*.") is True

def test_single_char_dot():
    assert is_match("a", "a.") is False

def test_star_multiple_groups():
    assert is_match("aabbc", "a*b*c") is True

def test_star_multiple_groups_fail():
    assert is_match("aabbcd", "a*b*c") is False

def test_all_stars():
    assert is_match("abcdef", "a*b*c*d*e*f*") is True

def test_pattern_longer_than_string():
    assert is_match("a", "aa") is False

def test_dot_star_matches_anything():
    assert is_match("anylongstring123", ".*") is True
