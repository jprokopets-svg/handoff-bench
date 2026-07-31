import pytest
from regex_parser import is_match


class TestBasicMatching:
    """Test basic character matching"""
    
    def test_exact_match(self):
        assert is_match("aa", "aa") == True
    
    def test_exact_mismatch(self):
        assert is_match("aa", "a") == False
    
    def test_empty_string_empty_pattern(self):
        assert is_match("", "") == True
    
    def test_empty_string_nonempty_pattern(self):
        assert is_match("", "a") == False
    
    def test_nonempty_string_empty_pattern(self):
        assert is_match("a", "") == False


class TestDotWildcard:
    """Test '.' wildcard matching"""
    
    def test_dot_matches_single_char(self):
        assert is_match("a", ".") == True
    
    def test_dot_matches_any_char(self):
        assert is_match("b", ".") == True
    
    def test_dot_matches_multiple(self):
        assert is_match("abc", "...") == True
    
    def test_dot_with_literals(self):
        assert is_match("abc", "a.c") == True
    
    def test_dot_mismatch_length(self):
        assert is_match("ab", "...") == False


class TestStarQuantifier:
    """Test '*' quantifier (zero or more)"""
    
    def test_star_zero_matches(self):
        assert is_match("b", "a*b") == True
    
    def test_star_one_match(self):
        assert is_match("ab", "a*b") == True
    
    def test_star_multiple_matches(self):
        assert is_match("aaab", "a*b") == True
    
    def test_star_mismatch(self):
        assert is_match("b", "a*c") == False
    
    def test_star_at_end_zero_matches(self):
        assert is_match("a", "a*") == True
    
    def test_star_at_end_multiple_matches(self):
        assert is_match("aaa", "a*") == True
    
    def test_star_at_end_mismatch(self):
        assert is_match("b", "a*") == False
    
    def test_multiple_stars(self):
        assert is_match("aabb", "a*b*") == True
    
    def test_multiple_stars_complex(self):
        assert is_match("aaabbbccc", "a*b*c*") == True
    
    def test_star_with_dot(self):
        assert is_match("aaa", ".*") == True
    
    def test_star_with_dot_any_string(self):
        assert is_match("abc", ".*") == True
    
    def test_star_with_dot_empty(self):
        assert is_match("", ".*") == True


class TestComplexPatterns:
    """Test complex pattern combinations"""
    
    def test_pattern_with_star_and_literal(self):
        assert is_match("mississippi", "mis*is*p*.") == True
    
    def test_pattern_mismatch_complex(self):
        assert is_match("aa", "a") == False
    
    def test_pattern_mismatch_star(self):
        assert is_match("aa", "a*b") == False
    
    def test_pattern_dot_star_combination(self):
        assert is_match("ab", ".*") == True
    
    def test_pattern_alternating_chars_and_stars(self):
        assert is_match("aabbbcd", "a*b*c*d") == True
    
    def test_pattern_with_leading_star_pattern(self):
        assert is_match("aab", "c*a*b") == True
    
    def test_pattern_exact_with_star(self):
        assert is_match("aa", "a*a") == True
    
    def test_pattern_star_greedy_behavior(self):
        # Star should match greedily but also allow backtracking
        assert is_match("aab", "a*ab") == True
    
    def test_pattern_star_with_multiple_same_chars(self):
        assert is_match("aaaa", "a*a*a*a*") == True


class TestEdgeCases:
    """Test edge cases"""
    
    def test_single_char_match(self):
        assert is_match("a", "a") == True
    
    def test_single_char_mismatch(self):
        assert is_match("a", "b") == False
    
    def test_long_string_with_star(self):
        assert is_match("aaaaaaaaaa", "a*") == True
    
    def test_pattern_only_stars(self):
        assert is_match("", "a*b*c*") == True
    
    def test_pattern_only_dots(self):
        assert is_match("abc", "...") == True
    
    def test_pattern_dot_star_only(self):
        assert is_match("anything", ".*") == True
