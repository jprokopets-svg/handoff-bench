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
        """Test when the entire string is a single word in dictionary."""
        assert word_break("hello", ["hello"]) is True
    
    def test_single_word_no_match(self):
        """Test when the entire string is not in dictionary."""
        assert word_break("hello", ["world"]) is False
    
    def test_empty_string(self):
        """Test with empty string."""
        assert word_break("", []) is True
    
    def test_empty_dictionary(self):
        """Test with empty dictionary."""
        assert word_break("hello", []) is False
    
    def test_multiple_valid_segmentations(self):
        """Test string with multiple possible valid segmentations."""
        assert word_break("applepenapple", ["apple", "pen"]) is True
    
    def test_case_sensitive(self):
        """Test that matching is case-sensitive."""
        assert word_break("Hello", ["hello"]) is False
    
    def test_overlapping_words(self):
        """Test with overlapping word patterns."""
        assert word_break("aaab", ["aa", "aaa", "b"]) is True
    
    def test_no_valid_segmentation(self):
        """Test when no valid segmentation exists."""
        assert word_break("abcd", ["a", "b", "c"]) is False
    
    def test_long_string(self):
        """Test with a longer string."""
        assert word_break("abcdefghij", ["ab", "cd", "ef", "gh", "ij"]) is True
    
    def test_repeated_words(self):
        """Test with repeated words in dictionary."""
        assert word_break("catcat", ["cat"]) is True
    
    def test_single_character_words(self):
        """Test with single character words."""
        assert word_break("abc", ["a", "b", "c"]) is True
    
    def test_greedy_approach_fails(self):
        """Test case where greedy approach would fail but DP succeeds."""
        # "catsandog" cannot be segmented even though "cat" and "cats" both exist
        assert word_break("catsandog", ["cat", "cats", "and", "sand", "dog"]) is False
    
    def test_word_at_end(self):
        """Test where valid word is only at the end."""
        assert word_break("abcd", ["ab", "cd"]) is True
    
    def test_dictionary_with_duplicates(self):
        """Test that duplicate words in dictionary don't cause issues."""
        assert word_break("hello", ["hello", "hello", "world"]) is True
