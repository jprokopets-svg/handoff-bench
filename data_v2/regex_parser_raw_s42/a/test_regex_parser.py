import pytest
from regex_parser import is_match


class TestRegexParser:
    """Test cases for regex pattern matching"""
    
    def test_empty_string_empty_pattern(self):
        """Empty string should match empty pattern"""
        assert is_match("", "") == True
    
    def test_empty_string_non_empty_pattern(self):
        """Empty string should not match non-empty pattern"""
        assert is_match("", "a") == False
    
    def test_simple_match(self):
        """Simple character matching"""
        assert is_match("a", "a") == True
        assert is_match("a", "b") == False
    
    def test_dot_matches_any_char(self):
        """Dot should match any single character"""
        assert is_match("a", ".") == True
        assert is_match("b", ".") == True
        assert is_match("", ".") == False
    
    def test_star_zero_occurrences(self):
        """Star should match zero occurrences"""
        assert is_match("", "a*") == True
        assert is_match("", ".*") == True
    
    def test_star_multiple_occurrences(self):
        """Star should match multiple occurrences"""
        assert is_match("aaa", "a*") == True
        assert is_match("bbb", "b*") == True
    
    def test_dot_star_matches_anything(self):
        """Dot star should match any string"""
        assert is_match("abc", ".*") == True
        assert is_match("", ".*") == True
        assert is_match("xyz", ".*") == True
    
    def test_complex_patterns(self):
        """Complex pattern matching"""
        assert is_match("aa", "a") == False
        assert is_match("aa", "a*") == True
        assert is_match("ab", ".*") == True
        assert is_match("aab", "c*a*b") == True
        assert is_match("mississippi", "mis*is*p*.") == True
    
    def test_pattern_with_multiple_stars(self):
        """Patterns with multiple star operators"""
        assert is_match("ab", "a*b*") == True
        assert is_match("aab", "a*b*") == True
        assert is_match("aaab", "a*b*") == True
        assert is_match("abab", "a*b*") == False
    
    def test_no_match_cases(self):
        """Cases where pattern should not match"""
        assert is_match("aa", "a") == False
        assert is_match("ab", "a") == False
        assert is_match("aab", "a*b*c") == False
    
    def test_dot_with_star(self):
        """Dot with star in various positions"""
        assert is_match("a", ".*a") == True
        assert is_match("ba", ".*a") == True
        assert is_match("bac", ".*a.*") == True
    
    def test_edge_cases(self):
        """Edge cases"""
        assert is_match("a", "a*") == True
        assert is_match("", "a*b*c*") == True
        assert is_match("abc", "a*b*c*") == True
