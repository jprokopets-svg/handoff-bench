import pytest
from regex_parser import is_match


# --- Exact character matching ---
def test_exact_match_simple():
    assert is_match("aa", "aa") == True

def test_exact_match_fail():
    assert is_match("aa", "a") == False

def test_exact_match_single():
    assert is_match("a", "a") == True

def test_exact_match_single_fail():
    assert is_match("b", "a") == False

def test_exact_match_longer_pattern():
    assert is_match("a", "aa") == False

def test_exact_match_longer_string():
    assert is_match("abc", "abc") == True

def test_exact_match_longer_string_fail():
    assert is_match("abc", "abd") == False


# --- Dot wildcard ---
def test_dot_matches_any_single_char():
    assert is_match("a", ".") == True

def test_dot_matches_any_single_char2():
    assert is_match("z", ".") == True

def test_dot_does_not_match_multiple():
    assert is_match("aa", ".") == False

def test_dot_in_middle():
    assert is_match("abc", "a.c") == True

def test_dot_in_middle_fail():
    assert is_match("ac", "a.c") == False

def test_all_dots():
    assert is_match("abc", "...") == True

def test_all_dots_fail():
    assert is_match("ab", "...") == False


# --- Star operator ---
def test_star_zero_matches():
    assert is_match("", "a*") == True

def test_star_zero_matches_nonempty_string():
    assert is_match("b", "a*b") == True

def test_star_one_match():
    assert is_match("a", "a*") == True

def test_star_multiple_matches():
    assert is_match("aa", "a*") == True

def test_star_many_matches():
    assert is_match("aaaa", "a*") == True

def test_star_fail():
    assert is_match("ab", "a*") == False

def test_star_with_dot():
    assert is_match("", ".*") == True

def test_star_with_dot_any_string():
    assert is_match("abc", ".*") == True

def test_star_with_dot_long_string():
    assert is_match("xyzabc123", ".*") == True

def test_star_multiple_groups():
    assert is_match("aabb", "a*b*") == True

def test_star_multiple_groups2():
    assert is_match("aabb", "a*b*c*") == True

def test_star_multiple_groups_fail():
    assert is_match("aabbc", "a*b*") == False

def test_star_zero_of_each():
    assert is_match("", "a*b*c*") == True


# --- Empty string / pattern ---
def test_empty_string_empty_pattern():
    assert is_match("", "") == True

def test_empty_string_nonempty_pattern():
    assert is_match("", "a") == False

def test_nonempty_string_empty_pattern():
    assert is_match("a", "") == False

def test_empty_string_dot():
    assert is_match("", ".") == False


# --- Combined patterns ---
def test_combined_dot_star():
    assert is_match("abc", "a.*") == True

def test_combined_dot_star2():
    assert is_match("abc", ".*c") == True

def test_combined_dot_star_fail():
    assert is_match("abc", ".*d") == False

def test_combined_complex():
    assert is_match("aab", "c*a*b") == True

def test_combined_complex2():
    assert is_match("mississippi", "mis*is*p*.") == False

def test_combined_complex3():
    assert is_match("mississippi", "mis*is*ip*.") == True

def test_star_preceding_dot():
    assert is_match("aaa", "a.a") == True

def test_star_preceding_dot_fail():
    assert is_match("aa", "a.a") == False


# --- Edge cases ---
def test_repeated_star_groups():
    assert is_match("", "a*a*a*") == True

def test_single_char_star_dot():
    # "a*." means zero-or-more 'a's followed by exactly one any-char
    # "a" can be matched: a* matches zero 'a's, '.' matches 'a' -> True
    assert is_match("a", "a*.") == True

def test_single_char_star_dot_empty():
    # "a*." requires at least one character for the dot
    assert is_match("", "a*.") == False

def test_two_chars_star_dot():
    # "a*." on "aa": a* matches one 'a', '.' matches second 'a' -> True
    assert is_match("aa", "a*.") == True

def test_pattern_longer_than_string():
    assert is_match("a", "ab*") == True

def test_pattern_with_only_stars():
    # '*' without a preceding char is technically invalid, but let's handle gracefully
    # We skip this edge case as it's undefined behavior
    pass

def test_full_match_required():
    # Partial matches should NOT count
    assert is_match("aab", "a") == False
    assert is_match("aab", "aa") == False
    assert is_match("aab", "aab") == True
