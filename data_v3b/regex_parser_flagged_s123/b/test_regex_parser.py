import pytest
from regex_parser import is_match


class TestRegexParser:
    def test_empty_string_empty_pattern(self):
        assert is_match("", "") == True
    
    def test_exact_match(self):
        assert is_match("aa", "aa") == True
        assert is_match("ab", "aa") == False
    
    def test_dot_matches_any_char(self):
        assert is_match("aa", ".a") == True
        assert is_match("ba", ".a") == True
        assert is_match("a", ".") == True
        assert is_match("ab", ".") == False
    
    def test_star_zero_occurrences(self):
        assert is_match("a", "a*") == True
        assert is_match("", "a*") == True
    
    def test_star_multiple_occurrences(self):
        assert is_match("aa", "a*") == True
        assert is_match("aaa", "a*") == True
    
    def test_star_with_other_chars(self):
        assert is_match("ab", "a*b") == True
        assert is_match("aab", "a*b") == True
        assert is_match("aaab", "a*b") == True
        assert is_match("b", "a*b") == True
        assert is_match("ac", "a*b") == False
    
    def test_dot_star(self):
        assert is_match("abc", ".*") == True
        assert is_match("", ".*") == True
        assert is_match("a", ".*") == True
    
    def test_complex_patterns(self):
        assert is_match("aa", "a") == False
        assert is_match("aa", ".*") == True
        assert is_match("ab", ".*") == True
        assert is_match("aab", "c*a*b") == True
        assert is_match("mississippi", "mis*is*p*.") == False
        assert is_match("ab", ".*") == True
        assert is_match("aab", "c*a*b") == True
