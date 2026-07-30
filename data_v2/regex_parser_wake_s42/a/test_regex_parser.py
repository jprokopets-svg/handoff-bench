import pytest
from regex_parser import is_match


class TestRegexParser:
    """Test cases for the regex pattern matcher"""
    
    def test_exact_match(self):
        """Test exact string matching"""
        assert is_match("aa", "a") == False
        assert is_match("aa", "aa") == True
        assert is_match("aab", "aab") == True
    
    def test_dot_matches_any_char(self):
        """Test that '.' matches any single character"""
        assert is_match("aa", ".a") == True
        assert is_match("ba", ".a") == True
        assert is_match("ca", ".a") == True
        assert is_match("a", ".") == True
        assert is_match("b", ".") == True
    
    def test_star_matches_zero_or_more(self):
        """Test that '*' matches zero or more of preceding character"""
        assert is_match("aa", "a") == False
        assert is_match("aa", "a*") == True
        assert is_match("aaa", "a*") == True
        assert is_match("", "a*") == True
        assert is_match("b", "a*") == False
    
    def test_star_with_dot(self):
        """Test '.*' which matches any sequence of characters"""
        assert is_match("ab", ".*") == True
        assert is_match("aab", "c*a*b") == True
        assert is_match("mississippi", "mis*is*p*.") == True
    
    def test_complex_patterns(self):
        """Test complex pattern combinations"""
        assert is_match("ab", ".*") == True
        assert is_match("aa", "a") == False
        assert is_match("aa", "a*") == True
        assert is_match("ab", ".*") == True
        assert is_match("aab", "c*a*b") == True
        assert is_match("aaca", "ab*a*c*a") == True
        assert is_match("aa", "a*a") == True
        assert is_match("aa", ".*a") == True
    
    def test_edge_cases(self):
        """Test edge cases"""
        assert is_match("", "") == True
        assert is_match("a", "") == False
        assert is_match("", "a") == False
        assert is_match("", "a*") == True
        assert is_match("", ".*") == True
    
    def test_no_match(self):
        """Test cases that should not match"""
        assert is_match("aa", "a") == False
        assert is_match("ab", "a") == False
        assert is_match("ab", "a*b*c") == False
        assert is_match("aab", "a*b*c") == False
