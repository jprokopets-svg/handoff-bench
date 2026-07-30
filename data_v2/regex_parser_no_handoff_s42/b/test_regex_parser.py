import pytest
from regex_parser import is_match


class TestRegexParser:
    """Test cases for regex pattern matching"""
    
    def test_exact_match(self):
        """Test exact string matching"""
        assert is_match("aa", "a") == False
        assert is_match("aa", "aa") == True
        assert is_match("aab", "aa") == False
    
    def test_dot_matches_any_char(self):
        """Test that '.' matches any single character"""
        assert is_match("aa", ".a") == True
        assert is_match("ba", ".a") == True
        assert is_match("a", ".") == True
        assert is_match("b", ".") == True
        assert is_match("", ".") == False
    
    def test_star_matches_zero_or_more(self):
        """Test that '*' matches zero or more of preceding character"""
        assert is_match("aa", "a") == False
        assert is_match("aa", "a*") == True
        assert is_match("aaa", "a*") == True
        assert is_match("", "a*") == True
        assert is_match("b", "a*") == False
    
    def test_star_with_dot(self):
        """Test '.*' which matches any sequence"""
        assert is_match("ab", ".*") == True
        assert is_match("aab", "c*a*b") == True
        assert is_match("mississippi", "mis*is*p*.") == True
    
    def test_complex_patterns(self):
        """Test more complex patterns"""
        assert is_match("ab", ".*") == True
        assert is_match("aa", "a") == False
        assert is_match("aa", "a*") == True
        assert is_match("ab", ".*") == True
        assert is_match("aab", "c*a*b") == True
        assert is_match("aaca", "ab*a*c*a") == True
        assert is_match("aa", "a*a") == True
        assert is_match("a", "ab*") == True
    
    def test_edge_cases(self):
        """Test edge cases"""
        assert is_match("", "") == True
        assert is_match("a", "") == False
        assert is_match("", "a") == False
        assert is_match("", "a*") == True
        assert is_match("", ".*") == True
    
    def test_multiple_stars(self):
        """Test patterns with multiple stars"""
        assert is_match("aab", "a*a*b") == True
        assert is_match("aab", "a*b*") == True
        assert is_match("aab", "a*ab*") == True
    
    def test_no_match_cases(self):
        """Test cases that should not match"""
        assert is_match("aa", "a") == False
        assert is_match("ab", "a") == False
        assert is_match("ab", "b") == False
        assert is_match("aab", "a*b*c") == False
