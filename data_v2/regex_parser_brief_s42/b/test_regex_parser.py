import pytest
from regex_parser import is_match


class TestRegexParser:
    """Test cases for the regex pattern matcher"""
    
    def test_empty_string_empty_pattern(self):
        """Empty string should match empty pattern"""
        assert is_match("", "") == True
    
    def test_empty_string_non_empty_pattern(self):
        """Empty string should not match non-empty pattern without *"""
        assert is_match("", "a") == False
    
    def test_dot_matches_any_char(self):
        """'.' should match any single character"""
        assert is_match("a", ".") == True
        assert is_match("b", ".") == True
        assert is_match("", ".") == False
    
    def test_literal_char_match(self):
        """Literal characters should match exactly"""
        assert is_match("a", "a") == True
        assert is_match("a", "b") == False
        assert is_match("aa", "aa") == True
        assert is_match("ab", "aa") == False
    
    def test_star_zero_occurrences(self):
        """'*' should match zero occurrences of preceding char"""
        assert is_match("", "a*") == True
        assert is_match("", ".*") == True
        assert is_match("b", "a*b") == True
    
    def test_star_multiple_occurrences(self):
        """'*' should match multiple occurrences of preceding char"""
        assert is_match("a", "a*") == True
        assert is_match("aa", "a*") == True
        assert is_match("aaa", "a*") == True
        assert is_match("aaa", "a*a") == True
    
    def test_dot_star_combination(self):
        """'.*' should match any sequence of characters"""
        assert is_match("", ".*") == True
        assert is_match("a", ".*") == True
        assert is_match("abc", ".*") == True
        assert is_match("xyz", ".*") == True
    
    def test_complex_patterns(self):
        """Test complex pattern combinations"""
        assert is_match("aa", "a") == False
        assert is_match("aa", "a*") == True
        assert is_match("ab", ".*") == True
        assert is_match("aab", "c*a*b") == True
        assert is_match("mississippi", "mis*is*p*.") == False
        assert is_match("ab", ".*") == True
        assert is_match("aab", "a*ab") == True
    
    def test_pattern_with_multiple_stars(self):
        """Test patterns with multiple * operators"""
        assert is_match("", "a*b*c*") == True
        assert is_match("abc", "a*b*c*") == True
        assert is_match("aabbcc", "a*b*c*") == True
        assert is_match("abcabc", "a*b*c*") == False
    
    def test_dot_with_star(self):
        """Test '.' combined with '*'"""
        assert is_match("abc", "a.*c") == True
        assert is_match("ac", "a.*c") == True
        assert is_match("adc", "a.*c") == True
        assert is_match("ab", "a.*c") == False
    
    def test_edge_cases(self):
        """Test edge cases"""
        assert is_match("a", "ab*") == True
        assert is_match("ab", "ab*") == True
        assert is_match("abb", "ab*") == True
        assert is_match("ac", "ab*c") == True
        assert is_match("abc", "ab*c") == True
        assert is_match("abbc", "ab*c") == True
