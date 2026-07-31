import pytest
from regex_parser import matches


# --- Exact character matching ---
def test_exact_match_single_char():
    assert matches("a", "a") is True

def test_exact_match_no_match():
    assert matches("a", "b") is False

def test_exact_match_multiple_chars():
    assert matches("abc", "abc") is True

def test_exact_match_partial():
    assert matches("abc", "ab") is False

def test_exact_match_extra_text():
    assert matches("ab", "abc") is False


# --- Wildcard '.' ---
def test_dot_matches_any_char():
    assert matches(".", "x") is True

def test_dot_matches_any_char2():
    assert matches(".", "a") is True

def test_dot_no_match_empty():
    assert matches(".", "") is False

def test_dot_in_pattern():
    assert matches("a.c", "abc") is True

def test_dot_in_pattern_any_middle():
    assert matches("a.c", "axc") is True

def test_dot_in_pattern_no_match():
    assert matches("a.c", "ac") is False

def test_multiple_dots():
    assert matches("...", "abc") is True

def test_multiple_dots_wrong_length():
    assert matches("...", "ab") is False


# --- Star '*' quantifier ---
def test_star_zero_occurrences():
    assert matches("a*", "") is True

def test_star_one_occurrence():
    assert matches("a*", "a") is True

def test_star_multiple_occurrences():
    assert matches("a*", "aaa") is True

def test_star_no_match_wrong_char():
    assert matches("a*", "b") is False

def test_star_with_prefix():
    assert matches("ba*", "b") is True

def test_star_with_prefix_and_matches():
    assert matches("ba*", "baaa") is True

def test_star_with_suffix():
    assert matches("a*b", "b") is True

def test_star_with_suffix_and_matches():
    assert matches("a*b", "aaab") is True

def test_star_with_suffix_no_match():
    assert matches("a*b", "aaa") is False


# --- Dot-star '.*' ---
def test_dot_star_matches_empty():
    assert matches(".*", "") is True

def test_dot_star_matches_any_string():
    assert matches(".*", "anything") is True

def test_dot_star_matches_single_char():
    assert matches(".*", "x") is True

def test_dot_star_in_middle():
    assert matches("a.*b", "axxxb") is True

def test_dot_star_in_middle_empty_middle():
    assert matches("a.*b", "ab") is True

def test_dot_star_anchored():
    assert matches("a.*b", "axxxc") is False


# --- Empty pattern and text ---
def test_empty_pattern_empty_text():
    assert matches("", "") is True

def test_empty_pattern_nonempty_text():
    assert matches("", "a") is False

def test_nonempty_pattern_empty_text():
    assert matches("a", "") is False


# --- Multiple stars ---
def test_multiple_stars():
    assert matches("a*b*", "") is True

def test_multiple_stars_only_a():
    assert matches("a*b*", "aaa") is True

def test_multiple_stars_only_b():
    assert matches("a*b*", "bbb") is True

def test_multiple_stars_both():
    assert matches("a*b*", "aaabbb") is True

def test_multiple_stars_wrong_order():
    assert matches("a*b*", "bba") is False


# --- Complex patterns ---
def test_complex_pattern_1():
    assert matches("a.b*c", "axc") is True

def test_complex_pattern_2():
    assert matches("a.b*c", "axbbbc") is True

def test_complex_pattern_3():
    assert matches("a.b*c", "axd") is False

def test_complex_repeated_dot_star():
    assert matches(".*.*", "hello") is True

def test_star_only_pattern():
    # '*' with no preceding char is technically invalid input,
    # but we just test well-formed patterns here
    pass

def test_long_match():
    assert matches("a*b*c*", "aaabbbccc") is True

def test_long_no_match():
    assert matches("a*b*c*", "aaabbbcccd") is False

def test_pattern_longer_than_text():
    assert matches("abcde", "abc") is False

def test_interleaved_star_dot():
    assert matches("a.*c.*e", "abcde") is True

def test_interleaved_star_dot_no_match():
    assert matches("a.*c.*e", "abcdf") is False
