import pytest
from regex_parser import is_match


class TestRegexParser:
    def test_exact_match(self):
        assert is_match("aa", "a") == False
        assert is_match("a", "a") == True
        assert is_match("ab", "ab") == True
    
    def test_dot_matches_any_char(self):
        assert is_match("a", ".") == True
        assert is_match("b", ".") == True
        assert is_match("ab", "a.") == True
        assert is_match("ab", ".b") == True
        assert is_match("abc", "a.c") == True
    
    def test_star_matches_zero_or_more(self):
        assert is_match("", "a*") == True
        assert is_match("a", "a*") == True
        assert is_match("aa", "a*") == True
        assert is_match("aaa", "a*") == True
        assert is_match("b", "a*") == False
    
    def test_star_with_dot(self):
        assert is_match("", ".*") == True
        assert is_match("a", ".*") == True
        assert is_match("ab", ".*") == True
        assert is_match("abc", ".*") == True
    
    def test_complex_patterns(self):
        assert is_match("aa", "a") == False
        assert is_match("aa", "a*") == True
        assert is_match("ab", ".*") == True
        assert is_match("ab", "a.*") == True
        assert is_match("ab", "a.") == True
        assert is_match("aab", "c*a*b") == True
        assert is_match("mississippi", "mis*is*p*.") == False
        assert is_match("ab", ".*") == True
        assert is_match("aab", "a*b") == True
    
    def test_edge_cases(self):
        assert is_match("", "") == True
        assert is_match("a", "") == False
        assert is_match("", "a") == False
        assert is_match("", "a*") == True
        assert is_match("", "a*b*") == True
    
    def test_multiple_stars(self):
        assert is_match("aab", "a*a*b") == True
        assert is_match("aab", "a*ab") == True
        assert is_match("aab", "a*b*") == True
        assert is_match("ab", "a*b*") == True
        assert is_match("", "a*b*") == True
