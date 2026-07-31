import pytest
from regex_parser import is_match


class TestBasicMatching:
    """Test basic character matching without wildcards or quantifiers."""
    
    def test_exact_match(self):
        assert is_match("a", "a") == True
    
    def test_exact_match_multiple_chars(self):
        assert is_match("abc", "abc") == True
    
    def test_no_match_different_char(self):
        assert is_match("a", "b") == False
    
    def test_no_match_different_length(self):
        assert is_match("a", "ab") == False
    
    def test_empty_string_empty_pattern(self):
        assert is_match("", "") == True
    
    def test_empty_string_non_empty_pattern(self):
        assert is_match("", "a") == False


class TestDotWildcard:
    """Test '.' wildcard matching any single character."""
    
    def test_dot_matches_single_char(self):
        assert is_match("a", ".") == True
    
    def test_dot_matches_any_char(self):
        assert is_match("z", ".") == True
    
    def test_dot_matches_digit(self):
        assert is_match("5", ".") == True
    
    def test_dot_multiple_positions(self):
        assert is_match("abc", "...") == True
    
    def test_dot_mixed_with_chars(self):
        assert is_match("abc", "a.c") == True
    
    def test_dot_no_match_length_mismatch(self):
        assert is_match("a", "..") == False
    
    def test_dot_no_match_wrong_char(self):
        assert is_match("abc", "a.d") == False


class TestStarQuantifier:
    """Test '*' quantifier for zero or more matches."""
    
    def test_star_zero_matches(self):
        assert is_match("b", "a*b") == True
    
    def test_star_one_match(self):
        assert is_match("ab", "a*b") == True
    
    def test_star_multiple_matches(self):
        assert is_match("aaab", "a*b") == True
    
    def test_star_many_matches(self):
        assert is_match("aaaaaab", "a*b") == True
    
    def test_star_at_beginning(self):
        assert is_match("aaa", "a*") == True
    
    def test_star_at_beginning_zero_matches(self):
        assert is_match("", "a*") == True
    
    def test_star_no_match_wrong_char(self):
        assert is_match("b", "a*c") == False
    
    def test_star_no_match_extra_chars(self):
        assert is_match("aab", "a*b") == True
    
    def test_multiple_stars(self):
        assert is_match("aabbb", "a*b*") == True
    
    def test_multiple_stars_zero_matches(self):
        assert is_match("", "a*b*") == True
    
    def test_multiple_stars_complex(self):
        assert is_match("aaabbbccc", "a*b*c*") == True


class TestDotStar:
    """Test '.*' combination (any characters, zero or more)."""
    
    def test_dot_star_matches_anything(self):
        assert is_match("abc", ".*") == True
    
    def test_dot_star_empty_string(self):
        assert is_match("", ".*") == True
    
    def test_dot_star_single_char(self):
        assert is_match("a", ".*") == True
    
    def test_dot_star_with_suffix(self):
        assert is_match("abc", ".*c") == True
    
    def test_dot_star_with_prefix(self):
        assert is_match("abc", "a.*") == True
    
    def test_dot_star_with_prefix_and_suffix(self):
        assert is_match("abc", "a.*c") == True
    
    def test_dot_star_no_match_wrong_suffix(self):
        assert is_match("abc", ".*d") == False


class TestComplexPatterns:
    """Test complex combinations of patterns."""
    
    def test_pattern_a_dot_star_b(self):
        assert is_match("axxxb", "a.*b") == True
    
    def test_pattern_a_star_dot_star_b(self):
        assert is_match("aaaxyzb", "a*.*b") == True
    
    def test_pattern_with_multiple_quantifiers(self):
        assert is_match("mississippi", "mis*is*p*.") == True
    
    def test_pattern_ab_star_ac_star_a(self):
        assert is_match("aabaca", "ab*ac*a") == True
    
    def test_no_match_complex(self):
        assert is_match("aa", "a") == False
    
    def test_no_match_complex_2(self):
        assert is_match("aa", "a*b") == False


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_pattern_longer_than_string(self):
        assert is_match("a", "abc") == False
    
    def test_string_longer_than_pattern(self):
        assert is_match("abc", "a") == False
    
    def test_repeated_stars(self):
        assert is_match("aaa", "a*a*a*") == True
    
    def test_dot_at_end(self):
        assert is_match("abc", "ab.") == True
    
    def test_pattern_all_dots(self):
        assert is_match("abc", "...") == True
    
    def test_pattern_all_stars(self):
        assert is_match("aaa", "a*a*a*") == True
