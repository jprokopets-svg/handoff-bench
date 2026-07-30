import pytest
from regex_parser import is_match


class TestRegexParser:
    def test_empty_pattern_empty_string(self):
        assert is_match("", "") == True
    
    def test_empty_pattern_nonempty_string(self):
        assert is_match("a", "") == False
    
    def test_exact_match(self):
        assert is_match("aa", "aa") == True
    
    def test_exact_mismatch(self):
        assert is_match("aa", "ab") == False
    
    def test_dot_matches_any_char(self):
        assert is_match("aa", "a.") == True
        assert is_match("ab", "a.") == True
        assert is_match("ba", ".") == False
    
    def test_star_zero_matches(self):
        assert is_match("a", "ab*") == True
        assert is_match("aa", "ab*") == False
    
    def test_star_multiple_matches(self):
        assert is_match("abb", "ab*") == True
        assert is_match("abbb", "ab*") == True
    
    def test_star_with_dot(self):
        assert is_match("aa", "a.*") == True
        assert is_match("ab", "a.*") == True
        assert is_match("aab", "a.*") == True
    
    def test_complex_patterns(self):
        assert is_match("mississippi", "mis*is*p*.") == False
        assert is_match("aa", "a") == False
        assert is_match("aa", "a*") == True
        assert is_match("ab", ".*") == True
        assert is_match("aab", "c*a*b") == True
