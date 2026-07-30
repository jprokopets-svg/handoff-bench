import pytest
from regex_parser import is_match


class TestRegexParser:
    """Test cases for regex pattern matching"""
    
    def test_exact_match(self):
        """Test exact string matching"""
        assert is_match("aa", "a") == False
        assert is_match("a", "a") == True
        assert is_match("abc", "abc") == True
        
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
        
    def test_dot_star_combination(self):
        """Test combinations of '.' and '*'"""
        assert is_match("ab", ".*") == True
        assert is_match("aab", "c*a*b") == True
        assert is_match("mississippi", "mis*is*p*.") == False
        assert is_match("aa", "a") == False
        assert is_match("aa", "a*") == True
        
    def test_complex_patterns(self):
        """Test more complex patterns"""
        assert is_match("ab", ".*") == True
        assert is_match("aab", "c*a*b") == True
        assert is_match("aaca", "ab*a*c*a") == True
        assert is_match("aa", "a*") == True
        assert is_match("ab", ".*") == True
        
    def test_empty_string(self):
        """Test empty string matching"""
        assert is_match("", "") == True
        assert is_match("", "a*") == True
        assert is_match("", ".*") == True
        assert is_match("a", "") == False
        
    def test_star_at_beginning(self):
        """Test patterns with star at beginning (should not match)"""
        # '*' without preceding character should not be valid in standard regex
        # but we test the behavior
        assert is_match("a", "*a") == False
        
    def test_multiple_stars(self):
        """Test patterns with multiple stars"""
        assert is_match("aab", "a*a*b") == True
        assert is_match("aabb", "a*b*") == True
        assert is_match("aabb", "a*a*b*b*") == True
        
    def test_realistic_patterns(self):
        """Test realistic regex patterns"""
        assert is_match("mississippi", "mis*is*p*.") == False
        assert is_match("ab", ".*") == True
        assert is_match("aab", "c*a*b") == True
        assert is_match("aaca", "ab*a*c*a") == True
