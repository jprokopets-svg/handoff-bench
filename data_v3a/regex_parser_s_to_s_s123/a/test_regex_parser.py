import pytest
from regex_parser import is_match


# --- Exact matches (no special chars) ---
def test_exact_match_simple():
    assert is_match("abc", "abc") is True

def test_exact_match_empty():
    assert is_match("", "") is True

def test_exact_no_match():
    assert is_match("abc", "abd") is False

def test_exact_length_mismatch():
    assert is_match("ab", "abc") is False

def test_exact_length_mismatch_2():
    assert is_match("abc", "ab") is False


# --- Dot '.' wildcard ---
def test_dot_matches_any_char():
    assert is_match("a", ".") is True

def test_dot_matches_digit():
    assert is_match("5", ".") is True

def test_dot_in_middle():
    assert is_match("abc", "a.c") is True

def test_dot_does_not_match_empty():
    assert is_match("", ".") is False

def test_all_dots():
    assert is_match("xyz", "...") is True

def test_dots_wrong_length():
    assert is_match("xy", "...") is False


# --- Star '*' quantifier ---
def test_star_zero_occurrences():
    assert is_match("b", "a*b") is True

def test_star_one_occurrence():
    assert is_match("ab", "a*b") is True

def test_star_multiple_occurrences():
    assert is_match("aaab", "a*b") is True

def test_star_empty_string():
    assert is_match("", "a*") is True

def test_star_only_pattern_no_match():
    assert is_match("b", "a*") is False

def test_star_matches_all():
    assert is_match("aaa", "a*") is True

def test_star_with_dot():
    assert is_match("anything", ".*") is True

def test_star_with_dot_empty():
    assert is_match("", ".*") is True


# --- Combined patterns ---
def test_dot_star_prefix():
    assert is_match("xyzabc", ".*abc") is True

def test_dot_star_suffix():
    assert is_match("abcxyz", "abc.*") is True

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

def test_pattern_longer_than_string():
    assert is_match("a", "ab*") is True

def test_repeated_dot_star():
    assert is_match("abcdef", ".*.*") is True


# --- Edge cases ---
def test_empty_string_non_empty_pattern():
    assert is_match("", "a") is False

def test_non_empty_string_empty_pattern():
    assert is_match("a", "") is False

def test_single_char_match():
    assert is_match("a", "a") is True

def test_single_char_no_match():
    assert is_match("b", "a") is False

def test_star_eliminates_all():
    assert is_match("", "a*b*c*") is True

def test_star_with_preceding_dot_matches_any_repeat():
    assert is_match("zzzzz", ".*") is True

def test_no_match_extra_chars():
    assert is_match("abcd", "abc") is False
