import pytest
from regex_parser import is_match


class TestRegexParser:
    """Test cases for the regex pattern matcher."""
    
    def test_exact_match(self):
        """Test exact character matching."""
        assert is_match("a", "a") == True
        assert is_match("ab", "ab") == True
        assert is_match("a", "b") == False
        assert is_match("ab", "ba") == False
    
    def test_dot_wildcard(self):
        """Test '.' matches any single character."""
        assert is_match("a", ".") == True
        assert is_match("b", ".") == True
        assert is_match("ab", "a.") == True
        assert is_match("ab", ".b") == True
        assert is_match("ab", ".") == False  # dot matches only one char
        assert is_match("ab", "...") == False  # three dots but only two chars
    
    def test_star_quantifier(self):
        """Test '*' matches zero or more of preceding character."""
        assert is_match("aa", "a") == False
        assert is_match("aa", "a*") == True
        assert is_match("aaa", "a*") == True
        assert is_match("", "a*") == True  # zero occurrences
        assert is_match("b", "a*") == False
    
    def test_star_with_dot(self):
        """Test '*' with '.' wildcard."""
        assert is_match("ab", ".*") == True
        assert is_match("aab", ".*") == True
        assert is_match("abc", ".*") == True
        assert is_match("", ".*") == True
    
    def test_complex_patterns(self):
        """Test complex pattern combinations."""
        assert is_match("aab", "c*a*b") == True
        assert is_match("ab", ".*") == True
        assert is_match("aab", "a*a*b") == True
        assert is_match("aab", "a*ab") == True
        assert is_match("aab", "a*b") == True
    
    def test_mississippi(self):
        """Test the classic mississippi case."""
        assert is_match("mississippi", "mis*is*p*.") == False
        assert is_match("mississippi", "m.*iss*p*.") == True
    
    def test_empty_cases(self):
        """Test empty string and pattern cases."""
        assert is_match("", "") == True
        assert is_match("", "a") == False
        assert is_match("a", "") == False
        assert is_match("", "a*") == True
        assert is_match("", "a*b*") == True
    
    def test_multiple_stars(self):
        """Test patterns with multiple star quantifiers."""
        assert is_match("aabb", "a*b*") == True
        assert is_match("aabb", "a*a*b*b*") == True
        assert is_match("ab", "a*b*") == True
        assert is_match("ba", "a*b*") == False
    
    def test_dot_star_combinations(self):
        """Test combinations of '.' and '*'."""
        assert is_match("aab", ".*ab") == True
        assert is_match("aab", "a.*b") == True
        assert is_match("aab", "a.*") == True
        assert is_match("aab", ".*b") == True
