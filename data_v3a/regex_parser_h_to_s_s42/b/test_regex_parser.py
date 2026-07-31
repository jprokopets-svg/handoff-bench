import pytest
from regex_parser import is_match


# --- Basic literal matching ---
def test_exact_match():
    assert is_match("abc", "abc") == True

def test_no_match_different_chars():
    assert is_match("abc", "abd") == False

def test_no_match_different_length():
    assert is_match("ab", "abc") == False

def test_single_char_match():
    assert is_match("a", "a") == True

def test_single_char_no_match():
    assert is_match("a", "b") == False


# --- Empty string / pattern ---
def test_empty_string_empty_pattern():
    assert is_match("", "") == True

def test_empty_string_nonempty_pattern():
    assert is_match("", "a") == False

def test_nonempty_string_empty_pattern():
    assert is_match("a", "") == False

def test_empty_string_star_pattern():
    assert is_match("", "a*") == True

def test_empty_string_multi_star_pattern():
    assert is_match("", "a*b*c*") == True

def test_empty_string_dot_star():
    assert is_match("", ".*") == True


# --- Dot wildcard ---
def test_dot_matches_any_char():
    assert is_match("a", ".") == True

def test_dot_matches_any_char2():
    assert is_match("z", ".") == True

def test_dot_no_match_empty():
    assert is_match("", ".") == False

def test_dot_in_pattern():
    assert is_match("abc", "a.c") == True

def test_dot_in_pattern_no_match():
    assert is_match("ac", "a.c") == False

def test_all_dots():
    assert is_match("abc", "...") == True

def test_all_dots_wrong_length():
    assert is_match("ab", "...") == False


# --- Star quantifier ---
def test_star_zero_occurrences():
    assert is_match("b", "a*b") == True

def test_star_one_occurrence():
    assert is_match("ab", "a*b") == True

def test_star_multiple_occurrences():
    assert is_match("aaab", "a*b") == True

def test_star_no_match():
    assert is_match("aab", "c*a*b") == True

def test_star_only():
    assert is_match("aaa", "a*") == True

def test_star_only_no_match():
    assert is_match("aab", "a*") == False

def test_star_with_different_char():
    assert is_match("", "a*") == True

def test_multiple_stars():
    assert is_match("aabb", "a*b*") == True

def test_multiple_stars_empty():
    assert is_match("", "a*b*") == True


# --- Dot-star ---
def test_dot_star_matches_anything():
    assert is_match("anything", ".*") == True

def test_dot_star_matches_empty():
    assert is_match("", ".*") == True

def test_dot_star_in_middle():
    assert is_match("abcdef", "a.*f") == True

def test_dot_star_in_middle_no_match():
    assert is_match("abcdef", "a.*g") == False

def test_dot_star_prefix():
    assert is_match("xyzabc", ".*abc") == True


# --- Complex patterns ---
def test_complex_1():
    assert is_match("aa", "a") == False

def test_complex_2():
    assert is_match("aa", "a*") == True

def test_complex_3():
    assert is_match("ab", ".*") == True

def test_complex_4():
    assert is_match("aab", "c*a*b") == True

def test_complex_5():
    assert is_match("mississippi", "mis*is*p*.") == False

def test_complex_6():
    assert is_match("mississippi", "mis*is*ip*.") == True

def test_complex_7():
    assert is_match("aaa", "a*a") == True

def test_complex_8():
    assert is_match("aaa", "ab*a") == False

def test_complex_9():
    assert is_match("aaa", "ab*ac*a") == True

def test_complex_10():
    assert is_match("a", "ab*") == True

def test_complex_11():
    assert is_match("bbbba", ".*a*a") == True

def test_complex_12():
    assert is_match("", "c*c*") == True

def test_complex_13():
    assert is_match("abcd", "d*") == False

def test_complex_14():
    assert is_match("abcde", "a.c.*e") == True

def test_complex_15():
    assert is_match("abcde", "a.c.*f") == False
