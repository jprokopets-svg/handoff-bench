import pytest
from word_break import word_break


class TestWordBreak:
    """Test cases for the word_break function."""
    
    def test_basic_positive_case(self):
        """Test a string that can be segmented."""
        assert word_break("leetcode", ["leet", "code"]) is True
    
    def test_basic_negative_case(self):
        """Test a string that cannot be segmented."""
        assert word_break("catsandog", ["cat", "cats", "and", "sand", "dog"]) is False
    
    def test_empty_string(self):
        """Test with an empty string."""
        assert word_break("", ["a", "b"]) is True
    
    def test_single_character_match(self):
        """Test with a single character that matches."""
        assert word_break("a", ["a"]) is True
    
    def test_single_character_no_match(self):
        """Test with a single character that doesn't match."""
        assert word_break("a", ["b"]) is False
    
    def test_word_not_in_dictionary(self):
        """Test when the entire string is not in the dictionary."""
        assert word_break("hello", ["world"]) is False
    
    def test_multiple_segmentations(self):
        """Test a string with multiple possible segmentations."""
        assert word_break("applepenapple", ["apple", "pen"]) is True
    
    def test_overlapping_words(self):
        """Test with overlapping word patterns."""
        assert word_break("catsandcatsdog", ["cat", "cats", "and", "sand", "dog"]) is True
    
    def test_repeated_words(self):
        """Test with repeated words in the dictionary."""
        assert word_break("aaaa", ["a", "aa", "aaa"]) is True
    
    def test_long_string_no_match(self):
        """Test a longer string that cannot be segmented."""
        assert word_break("aaab", ["a", "aa", "aaa"]) is False
    
    def test_dictionary_as_set(self):
        """Test that the function works with a set as input."""
        assert word_break("leetcode", {"leet", "code"}) is True
    
    def test_complex_case(self):
        """Test a more complex segmentation."""
        assert word_break("pineapplepenapple", ["apple", "pen", "applepen", "pine", "pineapple"]) is True
    
    def test_no_valid_segmentation(self):
        """Test when no valid segmentation exists."""
        assert word_break("abcd", ["a", "b", "c"]) is False
