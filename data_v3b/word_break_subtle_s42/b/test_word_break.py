import pytest
from word_break import word_break


class TestWordBreak:
    """Test cases for the word_break function."""
    
    def test_basic_true_case(self):
        """Test basic case where string can be segmented."""
        assert word_break("leetcode", ["leet", "code"]) is True
    
    def test_basic_false_case(self):
        """Test basic case where string cannot be segmented."""
        assert word_break("catsandog", ["cat", "cats", "and", "sand", "dog"]) is False
    
    def test_single_word_match(self):
        """Test when string is exactly one word from dictionary."""
        assert word_break("hello", ["hello"]) is True
    
    def test_single_word_no_match(self):
        """Test when string doesn't match any single word."""
        assert word_break("hello", ["world"]) is False
    
    def test_empty_string(self):
        """Test empty string."""
        assert word_break("", []) is True
    
    def test_empty_dictionary(self):
        """Test with empty dictionary."""
        assert word_break("hello", []) is False
    
    def test_multiple_segmentations(self):
        """Test string with multiple possible segmentations."""
        assert word_break("applepenapple", ["apple", "pen"]) is True
    
    def test_repeated_words(self):
        """Test string with repeated words."""
        assert word_break("aaab", ["aa", "aaa", "b"]) is True
    
    def test_repeated_words_false(self):
        """Test string with repeated words that cannot be segmented."""
        assert word_break("aaaa", ["aaa", "b"]) is False
    
    def test_single_character(self):
        """Test single character string."""
        assert word_break("a", ["a"]) is True
    
    def test_single_character_no_match(self):
        """Test single character string with no match."""
        assert word_break("a", ["b"]) is False
    
    def test_longer_string(self):
        """Test longer string with multiple words."""
        assert word_break("catsandcatsdog", ["cat", "cats", "and", "sand", "dog"]) is True
    
    def test_overlapping_words(self):
        """Test with overlapping word possibilities."""
        assert word_break("abcd", ["ab", "abc", "cd", "def", "abcd"]) is True
    
    def test_word_dict_as_set(self):
        """Test that function works with set input."""
        assert word_break("leetcode", {"leet", "code"}) is True
    
    def test_case_sensitive(self):
        """Test that matching is case-sensitive."""
        assert word_break("Hello", ["hello"]) is False
    
    def test_complex_case(self):
        """Test complex case with many possibilities."""
        assert word_break("pineapplepenapple", ["apple", "pen", "applepen", "pine", "pineapple"]) is True
