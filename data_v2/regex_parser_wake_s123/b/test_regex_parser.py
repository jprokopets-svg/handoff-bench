import pytest
from regex_parser import is_match


class TestRegexMatcher:
    """Test cases for the regex pattern matcher."""
    
    def test_empty_string_empty_pattern(self):
        """Empty string should match empty pattern."""
        assert is_match("", "") == True
    
    def test_empty_string_non_empty_pattern(self):
        """Empty string should not match non-empty pattern (without *)."""
        assert is_match("", "a") == False
    
    def test_non_empty_string_empty_pattern(self):
        """Non-empty string should not match empty pattern."""
        assert is_match("a", "") == False
    
    def test_exact_match(self):
        """Exact character matches."""
        assert is_match("aa", "aa") == True
        assert is_match("ab", "ab") == True
    
    def test_exact_mismatch(self):
        """Exact character mismatches."""
        assert is_match("aa", "a") == False
        assert is_match("ab", "ba") == False
    
    def test_dot_wildcard_single(self):
        """'.' matches any single character."""
        assert is_match("a", ".") == True
        assert is_match("b", ".") == True
        assert is_match("aa", ".") == False
    
    def test_dot_wildcard_multiple(self):
        """'.' matches any character in sequence."""
        assert is_match("ab", "..") == True
        assert is_match("abc", "...") == True
        assert is_match("ab", "...") == False
    
    def test_star_zero_matches(self):
        """'*' matches zero occurrences of preceding character."""
        assert is_match("b", "a*b") == True
        assert is_match("aab", "a*ab") == True
    
    def test_star_one_or_more_matches(self):
        """'*' matches one or more occurrences of preceding character."""
        assert is_match("aa", "a*") == True
        assert is_match("aaa", "a*") == True
        assert is_match("aab", "a*b") == True
    
    def test_star_with_dot(self):
        """'.*' matches any sequence of characters."""
        assert is_match("ab", ".*") == True
        assert is_match("abc", ".*") == True
        assert is_match("", ".*") == True
    
    def test_complex_patterns(self):
        """Complex pattern matching."""
        assert is_match("aab", "c*a*b") == True
        assert is_match("ab", ".*") == True
        assert is_match("aab", "a*a*b") == True
        assert is_match("mississippi", "mis*is*p*.") == False
    
    def test_star_at_beginning_of_pattern(self):
        """Pattern starting with '*' should be handled (though unusual)."""
        # Note: In standard regex, '*' requires a preceding element
        # This tests edge case behavior
        pass
    
    def test_multiple_star_operators(self):
        """Multiple '*' operators in pattern."""
        assert is_match("aaaa", "a*a*") == True
        assert is_match("ab", "a*b*") == True
        assert is_match("aabb", "a*b*") == True
    
    def test_dot_and_star_combination(self):
        """Combining '.' and '*' operators."""
        assert is_match("abc", "a.*c") == True
        assert is_match("ac", "a.*c") == True
        assert is_match("adc", "a.*c") == True
    
    def test_no_match_cases(self):
        """Cases that should not match."""
        assert is_match("aa", "a") == False
        assert is_match("ab", "a") == False
        assert is_match("aab", "a*b*c") == False
