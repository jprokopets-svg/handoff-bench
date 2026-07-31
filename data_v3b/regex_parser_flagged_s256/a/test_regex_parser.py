import pytest
from regex_parser import is_match


class TestRegexParser:
    """Test cases for the regex pattern matcher."""

    def test_empty_pattern_empty_string(self):
        """Empty pattern should match empty string."""
        assert is_match("", "") == True

    def test_empty_pattern_nonempty_string(self):
        """Empty pattern should not match non-empty string."""
        assert is_match("a", "") == False

    def test_nonempty_pattern_empty_string(self):
        """Non-empty pattern should not match empty string (unless it's all *)."""
        assert is_match("", "a") == False

    def test_literal_match(self):
        """Literal characters should match exactly."""
        assert is_match("a", "a") == True
        assert is_match("ab", "ab") == True
        assert is_match("a", "b") == False

    def test_dot_matches_any_char(self):
        """Dot should match any single character."""
        assert is_match("a", ".") == True
        assert is_match("b", ".") == True
        assert is_match("ab", ".") == False
        assert is_match("ab", "a.") == True
        assert is_match("ab", ".b") == True
        assert is_match("ab", "..") == True

    def test_star_zero_matches(self):
        """Star should match zero occurrences of preceding character."""
        assert is_match("", "a*") == True
        assert is_match("", ".*") == True
        assert is_match("b", "a*") == False

    def test_star_one_or_more_matches(self):
        """Star should match one or more occurrences of preceding character."""
        assert is_match("a", "a*") == True
        assert is_match("aa", "a*") == True
        assert is_match("aaa", "a*") == True
        assert is_match("b", "a*b") == True
        assert is_match("ab", "a*b") == True
        assert is_match("aab", "a*b") == True
        assert is_match("aaab", "a*b") == True

    def test_dot_star_matches_anything(self):
        """Dot star should match any sequence of characters."""
        assert is_match("", ".*") == True
        assert is_match("a", ".*") == True
        assert is_match("abc", ".*") == True
        assert is_match("xyz", ".*") == True

    def test_complex_patterns(self):
        """Test more complex pattern combinations."""
        assert is_match("aa", "a") == False
        assert is_match("aa", "a*") == True
        assert is_match("ab", ".*") == True
        assert is_match("aab", "c*a*b") == True
        assert is_match("mississippi", "mis*is*p*.") == False
        assert is_match("ab", ".*") == True
        assert is_match("aab", "c*a*b") == True

    def test_pattern_with_multiple_stars(self):
        """Test patterns with multiple star operators."""
        assert is_match("", "a*b*c*") == True
        assert is_match("abc", "a*b*c*") == True
        assert is_match("aabbcc", "a*b*c*") == True
        assert is_match("abcabc", "a*b*c*") == False

    def test_no_match_cases(self):
        """Test cases that should not match."""
        assert is_match("aa", "a") == False
        assert is_match("ab", "a") == False
        assert is_match("ba", "ab") == False
