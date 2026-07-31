"""Tests for regex_parser.py"""
import pytest
from regex_parser import is_match


# --- Basic literal matching ---
def test_exact_match():
    assert is_match("abc", "abc") is True

def test_no_match_different_chars():
    assert is_match("abc", "abd") is False

def test_empty_string_empty_pattern():
    assert is_match("", "") is True

def test_empty_string_nonempty_pattern():
    assert is_match("", "a") is False

def test_nonempty_string_empty_pattern():
    assert is_match("a", "") is False


# --- Dot '.' matching ---
def test_dot_matches_any_char():
    assert is_match("a", ".") is True

def test_dot_matches_any_char2():
    assert is_match("z", ".") is True

def test_dot_in_middle():
    assert is_match("abc", "a.c") is True

def test_dot_does_not_match_empty():
    assert is_match("", ".") is False

def test_all_dots():
    assert is_match("abc", "...") is True

def test_all_dots_wrong_length():
    assert is_match("ab", "...") is False


# --- Star '*' matching ---
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

def test_dot_star_matches_anything():
    assert is_match("anything", ".*") is True

def test_dot_star_matches_empty():
    assert is_match("", ".*") is True

def test_multiple_stars():
    assert is_match("aabb", "a*b*") is True

def test_multiple_stars_empty():
    assert is_match("", "a*b*") is True

def test_star_with_dot():
    assert is_match("xyzabc", ".*abc") is True


# --- Combined patterns ---
def test_combined_1():
    assert is_match("mississippi", "mis*is*p*.") is False

def test_combined_2():
    assert is_match("aab", "c*a*b") is True

def test_combined_3():
    assert is_match("aa", "a*") is True

def test_combined_4():
    assert is_match("aa", "a") is False

def test_combined_5():
    assert is_match("aa", "aa") is True

def test_combined_6():
    assert is_match("ab", ".*") is True

def test_combined_7():
    assert is_match("ab", ".*c") is False

def test_combined_8():
    assert is_match("aaa", "a*a") is True

def test_combined_9():
    assert is_match("", "c*c*") is True

def test_combined_10():
    assert is_match("a", "ab*") is True  # b* = zero b's
