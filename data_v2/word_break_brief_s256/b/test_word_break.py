import pytest
from word_break import word_break


class TestWordBreak:
    """Test cases for the word_break function."""
    
    def test_basic_positive_case(self):
        """Test basic case where string can be segmented."""
        assert word_break("leetcode", ["leet", "code"]) is True
    
    def test_basic_negative_case(self):
        """Test basic case where string cannot be segmented."""
        assert word_break("catsandog", ["cat", "cats", "and", "sand", "dog"]) is False
    
    def test_empty_string(self):
        """Test empty string - should return True."""
        assert word_break("", []) is True
    
    def test_single_character_match(self):
        """Test single character that matches dictionary."""
        assert word_break("a", ["a"]) is True
    
    def test_single_character_no_match(self):
        """Test single character that doesn't match dictionary."""
        assert word_break("a", ["b"]) is False
    
    def test_empty_dictionary(self):
        """Test with empty dictionary - only empty string should work."""
        assert word_break("", []) is True
        assert word_break("a", []) is False
    
    def test_overlapping_words(self):
        """Test with overlapping words in dictionary."""
        assert word_break("applepenapple", ["apple", "pen"]) is True
    
    def test_no_valid_segmentation(self):
        """Test case where no valid segmentation exists."""
        assert word_break("catsandog", ["cat", "cats", "and", "sand", "dog"]) is False
    
    def test_multiple_valid_segmentations(self):
        """Test case with multiple possible segmentations."""
        assert word_break("pineapplepenapple", ["pine", "pineapple", "apple", "pen"]) is True
    
    def test_word_appears_multiple_times(self):
        """Test where same word appears multiple times in segmentation."""
        assert word_break("aaaa", ["a", "aa"]) is True
    
    def test_long_string_no_match(self):
        """Test longer string that cannot be segmented."""
        assert word_break("aaaaaab", ["a", "aa"]) is False
    
    def test_case_sensitive(self):
        """Test that matching is case-sensitive."""
        assert word_break("Leetcode", ["leet", "code"]) is False
        assert word_break("leetcode", ["Leet", "Code"]) is False
    
    def test_word_dict_as_set(self):
        """Test that function works with set input."""
        assert word_break("leetcode", {"leet", "code"}) is True
    
    def test_repeated_substrings(self):
        """Test with repeated substrings."""
        assert word_break("aaaa", ["aaa", "a"]) is True
        assert word_break("aaaa", ["aaa"]) is False
