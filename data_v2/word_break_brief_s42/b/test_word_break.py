import pytest
from word_break import word_break


class TestWordBreak:
    """Test cases for the word_break function."""
    
    def test_valid_segmentation_basic(self):
        """Test a basic valid segmentation."""
        assert word_break("catsanddog", ["cat", "cats", "and", "sand", "dog"]) == True
    
    def test_invalid_segmentation(self):
        """Test an invalid segmentation."""
        assert word_break("catsandog", ["cat", "cats", "and", "sand", "dog"]) == False
    
    def test_empty_string(self):
        """Test with empty string."""
        assert word_break("", ["cat", "dog"]) == True
    
    def test_single_word_match(self):
        """Test with a single word that matches."""
        assert word_break("cat", ["cat"]) == True
    
    def test_single_word_no_match(self):
        """Test with a single word that doesn't match."""
        assert word_break("cat", ["dog"]) == False
    
    def test_empty_dictionary(self):
        """Test with empty dictionary."""
        assert word_break("cat", []) == False
    
    def test_empty_dictionary_empty_string(self):
        """Test with empty dictionary and empty string."""
        assert word_break("", []) == True
    
    def test_multiple_valid_segmentations(self):
        """Test string with multiple possible valid segmentations."""
        assert word_break("pineapplepenapple", ["apple", "pen", "applepen", "pine", "pineapple"]) == True
    
    def test_overlapping_words(self):
        """Test with overlapping word patterns."""
        assert word_break("leetcode", ["leet", "code"]) == True
    
    def test_no_valid_segmentation_with_similar_words(self):
        """Test where similar words exist but don't form valid segmentation."""
        assert word_break("applepenapple", ["apple", "pen"]) == True
    
    def test_long_string_valid(self):
        """Test with longer string."""
        assert word_break("aaaaaab", ["a", "aa", "aaa", "aaaa", "aaaaa", "aaaaaa"]) == False
    
    def test_long_string_valid_case(self):
        """Test with longer string that is valid."""
        assert word_break("aaaaaaa", ["a", "aa", "aaa", "aaaa", "aaaaa", "aaaaaa"]) == True
    
    def test_case_sensitive(self):
        """Test that matching is case-sensitive."""
        assert word_break("Cat", ["cat"]) == False
    
    def test_word_dict_as_set(self):
        """Test that function works with set input."""
        assert word_break("catsanddog", {"cat", "cats", "and", "sand", "dog"}) == True
