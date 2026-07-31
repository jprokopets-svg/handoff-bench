import pytest
from regex_parser import is_match


class TestBasicMatching:
    """Test basic character matching"""
    
    def test_exact_match(self):
        assert is_match("aa", "aa") == True
    
    def test_exact_no_match(self):
        assert is_match("aa", "a") == False
    
    def test_empty_string_empty_pattern(self):
        assert is_match("", "") == True
    
    def test_empty_string_non_empty_pattern(self):
        assert is_match("", "a") == False
    
    def test_non_empty_string_empty_pattern(self):
        assert is_match("a", "") == False


class TestDotWildcard:
    """Test '.' wildcard matching"""
    
    def test_dot_matches_single_char(self):
        assert is_match("aa", ".a") == True
    
    def test_dot_matches_any_char(self):
        assert is_match("ba", ".a") == True
    
    def test_dot_does_not_match_empty(self):
        assert is_match("a", ".") == True
    
    def test_multiple_dots(self):
        assert is_match("abc", "...") == True
    
    def test_dot_length_mismatch(self):
        assert is_match("ab", "...") == False


class TestStarQuantifier:
    """Test '*' quantifier matching"""
    
    def test_star_zero_matches(self):
        assert is_match("aa", "a*aa") == True
    
    def test_star_one_match(self):
        assert is_match("aa", "aa*") == True
    
    def test_star_multiple_matches(self):
        assert is_match("aaa", "a*") == True
    
    def test_star_zero_occurrences(self):
        assert is_match("b", "a*b") == True
    
    def test_star_multiple_occurrences(self):
        assert is_match("aaab", "a*b") == True
    
    def test_star_no_match(self):
        assert is_match("b", "a*c") == False


class TestCombined:
    """Test combined patterns with '.' and '*'"""
    
    def test_dot_star_any_sequence(self):
        assert is_match("abc", ".*") == True
    
    def test_dot_star_empty(self):
        assert is_match("", ".*") == True
    
    def test_dot_star_with_literal(self):
        assert is_match("aab", "a*b") == True
    
    def test_complex_pattern_1(self):
        assert is_match("aa", "a") == False
    
    def test_complex_pattern_2(self):
        assert is_match("aa", "a*") == True
    
    def test_complex_pattern_3(self):
        assert is_match("ab", ".*") == True
    
    def test_complex_pattern_4(self):
        assert is_match("aab", "c*a*b") == True
    
    def test_complex_pattern_5(self):
        assert is_match("mississippi", "mis*is*p*.") == False


class TestEdgeCases:
    """Test edge cases"""
    
    def test_star_at_beginning(self):
        assert is_match("aaa", "a*aaa") == True
    
    def test_multiple_stars(self):
        assert is_match("aabb", "a*b*") == True
    
    def test_star_with_dot(self):
        assert is_match("aab", ".*ab") == True
    
    def test_pattern_longer_than_string(self):
        assert is_match("a", "aaa") == False
    
    def test_single_char_pattern(self):
        assert is_match("a", "a") == True
    
    def test_single_dot_pattern(self):
        assert is_match("x", ".") == True
