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
    
    def test_non_empty_string_empty_pattern(self):
        """Non-empty string should not match empty pattern"""
        assert is_match("a", "") == False
    
    def test_exact_match(self):
        """Exact character matches"""
        assert is_match("a", "a") == True
        assert is_match("ab", "ab") == True
        assert is_match("abc", "abc") == True
    
    def test_exact_mismatch(self):
        """Exact character mismatches"""
        assert is_match("a", "b") == False
        assert is_match("ab", "ac") == False
    
    def test_dot_single_char(self):
        """Dot matches any single character"""
        assert is_match("a", ".") == True
        assert is_match("b", ".") == True
        assert is_match("z", ".") == True
    
    def test_dot_multiple_chars(self):
        """Dot matches any character in sequence"""
        assert is_match("abc", "...") == True
        assert is_match("xyz", "...") == True
        assert is_match("a", "..") == False
    
    def test_dot_with_literals(self):
        """Dot mixed with literal characters"""
        assert is_match("ab", "a.") == True
        assert is_match("ac", "a.") == True
        assert is_match("abc", "a.c") == True
        assert is_match("adc", "a.c") == True
    
    def test_star_zero_matches(self):
        """Star matches zero occurrences"""
        assert is_match("", "a*") == True
        assert is_match("", "ab*") == False
        assert is_match("a", "ab*") == True
    
    def test_star_one_match(self):
        """Star matches one occurrence"""
        assert is_match("a", "a*") == True
        assert is_match("b", "a*b") == False
        assert is_match("ab", "a*b") == True
    
    def test_star_multiple_matches(self):
        """Star matches multiple occurrences"""
        assert is_match("aa", "a*") == True
        assert is_match("aaa", "a*") == True
        assert is_match("aaaa", "a*") == True
    
    def test_star_with_literals(self):
        """Star with literal characters"""
        assert is_match("aab", "a*b") == True
        assert is_match("aaab", "a*b") == True
        assert is_match("b", "a*b") == True
        assert is_match("ac", "a*b") == False
    
    def test_multiple_stars(self):
        """Multiple star patterns"""
        assert is_match("", "a*b*") == True
        assert is_match("a", "a*b*") == True
        assert is_match("b", "a*b*") == True
        assert is_match("ab", "a*b*") == True
        assert is_match("aab", "a*b*") == True
        assert is_match("abb", "a*b*") == True
        assert is_match("aabb", "a*b*") == True
    
    def test_dot_star_combination(self):
        """Dot with star"""
        assert is_match("", ".*") == True
        assert is_match("a", ".*") == True
        assert is_match("abc", ".*") == True
        assert is_match("xyz", ".*") == True
    
    def test_dot_star_with_literals(self):
        """Dot star with literal characters"""
        assert is_match("abc", "a.*c") == True
        assert is_match("ac", "a.*c") == True
        assert is_match("adc", "a.*c") == True
        assert is_match("adec", "a.*c") == True
    
    def test_complex_patterns(self):
        """Complex pattern combinations"""
        assert is_match("aa", "a") == False
        assert is_match("aa", "a*") == True
        assert is_match("ab", ".*") == True
        assert is_match("aab", "c*a*b") == True
        assert is_match("mississippi", "mis*is*p*.") == False
        assert is_match("ab", ".*") == True
        assert is_match("aab", "c*a*b") == True
    
    def test_edge_cases(self):
        """Edge cases"""
        assert is_match("a", "a*a") == True
        assert is_match("aa", "a*a") == True
        assert is_match("aaa", "a*a") == True
        assert is_match("", "a*a*") == True
