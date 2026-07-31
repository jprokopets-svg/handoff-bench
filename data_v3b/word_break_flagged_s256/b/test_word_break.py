import pytest
from word_break import word_break


class TestWordBreak:
    """Test cases for the word_break function."""
    
    def test_basic_true_case(self):
        """Test a simple case where string can be segmented."""
        assert word_break("leetcode", ["leet", "code"]) is True
    
    def test_basic_false_case(self):
        """Test a simple case where string cannot be segmented."""
        assert word_break("catsandog", ["cat", "cats", "and", "sand", "dog"]) is False
    
    def test_empty_string(self):
        """Test empty string."""
        assert word_break("", []) is True
    
    def test_empty_dict(self):
        """Test with empty dictionary."""
        assert word_break("hello", []) is False
    
    def test_single_word_match(self):
        """Test when string matches a single word exactly."""
        assert word_break("hello", ["hello"]) is True
    
    def test_single_word_no_match(self):
        """Test when string doesn't match any word."""
        assert word_break("hello", ["world"]) is False
    
    def test_multiple_segmentations(self):
        """Test string that can be segmented multiple ways."""
        assert word_break("catsandcatsdog", ["cat", "cats", "and", "sand", "dog"]) is True
    
    def test_overlapping_words(self):
        """Test with overlapping word prefixes."""
        assert word_break("applepenapple", ["apple", "pen"]) is True
    
    def test_no_valid_segmentation(self):
        """Test when no valid segmentation exists."""
        assert word_break("catsandog", ["cat", "cats", "and", "sand", "dog"]) is False
    
    def test_long_string(self):
        """Test with a longer string."""
        assert word_break("aaaaaab", ["a", "aa", "aaa", "aaaa", "aaaaa"]) is False
    
    def test_long_string_valid(self):
        """Test with a longer string that can be segmented."""
        assert word_break("aaaaaaa", ["a", "aa", "aaa", "aaaa", "aaaaa"]) is True
    
    def test_single_character_words(self):
        """Test with single character words."""
        assert word_break("abc", ["a", "b", "c"]) is True
    
    def test_case_sensitive(self):
        """Test that matching is case-sensitive."""
        assert word_break("Hello", ["hello"]) is False
    
    def test_word_dict_as_set(self):
        """Test that function works with set input."""
        assert word_break("leetcode", {"leet", "code"}) is True
    
    def test_repeated_words(self):
        """Test with repeated words in dictionary."""
        assert word_break("aa", ["a", "a"]) is True
