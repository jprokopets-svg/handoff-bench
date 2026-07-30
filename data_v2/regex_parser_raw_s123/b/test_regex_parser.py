import pytest
from regex_parser import is_match


class TestRegexParser:
    """Test cases for regex pattern matching"""
    
    def test_exact_match(self):
        """Test exact string matching"""
        assert is_match("aa", "a") == False
        assert is_match("a", "a") == True
        assert is_match("ab", "ab") == True
        assert is_match("abc", "abc") == True
    
    def test_dot_matches_any_char(self):
        """Test that '.' matches any single character"""
        assert is_match("a", ".") == True
        assert is_match("b", ".") == True
        assert is_match("", ".") == False
        assert is_match("ab", "a.") == True
        assert is_match("ac", "a.") == True
        assert is_match("aa", "a.") == True
        assert is_match("ba", ".a") == True
    
    def test_star_zero_matches(self):
        """Test that '*' matches zero occurrences"""
        assert is_match("a", "ab*") == True
        assert is_match("", "a*") == True
        assert is_match("", ".*") == True
        assert is_match("aaa", "a*") == True
    
    def test_star_multiple_matches(self):
        """Test that '*' matches multiple occurrences"""
        assert is_match("aa", "a*") == True
        assert is_match("aaa", "a*") == True
        assert is_match("aaaa", "a*") == True
        assert is_match("ab", "a*b") == True
        assert is_match("aab", "a*b") == True
        assert is_match("aaab", "a*b") == True
    
    def test_dot_star_combination(self):
        """Test combinations of '.' and '*'"""
        assert is_match("abc", "a.*c") == True
        assert is_match("ac", "a.*c") == True
        assert is_match("adc", "a.*c") == True
        assert is_match("addc", "a.*c") == True
        assert is_match("", ".*") == True
        assert is_match("a", ".*") == True
        assert is_match("abc", ".*") == True
    
    def test_complex_patterns(self):
        """Test more complex patterns"""
        assert is_match("aa", "a") == False
        assert is_match("aa", "a*") == True
        assert is_match("ab", ".*") == True
        assert is_match("aab", "c*a*b") == True
        assert is_match("mississippi", "mis*is*p*.") == False
        assert is_match("ab", ".*") == True
    
    def test_no_match(self):
        """Test cases that should not match"""
        assert is_match("aa", "a") == False
        assert is_match("ab", "a") == False
        assert is_match("a", "b") == False
        assert is_match("abc", "ab") == False
        assert is_match("aab", "c*a*b") == True
        assert is_match("baa", "c*a*b") == False
    
    def test_edge_cases(self):
        """Test edge cases"""
        assert is_match("", "") == True
        assert is_match("a", "") == False
        assert is_match("", "a") == False
        assert is_match("", "a*") == True
        assert is_match("", ".*") == True
    
    def test_multiple_star_patterns(self):
        """Test patterns with multiple '*' operators"""
        assert is_match("a", "a*b*c*") == True
        assert is_match("ab", "a*b*c*") == True
        assert is_match("abc", "a*b*c*") == True
        assert is_match("aabbcc", "a*b*c*") == True
        assert is_match("aabbc", "a*b*c*") == True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
