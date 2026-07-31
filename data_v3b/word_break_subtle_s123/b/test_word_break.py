import pytest
from word_break import word_break


class TestWordBreak:
    """Test cases for the word_break function"""
    
    def test_basic_success_case(self):
        """Test basic case where string can be segmented"""
        assert word_break("leetcode", ["leet", "code"]) is True
    
    def test_basic_failure_case(self):
        """Test basic case where string cannot be segmented"""
        assert word_break("catsandog", ["cat", "cats", "and", "sand", "dog"]) is False
    
    def test_single_word_match(self):
        """Test when entire string is a single word in dictionary"""
        assert word_break("hello", ["hello"]) is True
    
    def test_single_word_no_match(self):
        """Test when entire string is not in dictionary"""
        assert word_break("hello", ["world"]) is False
    
    def test_empty_string(self):
        """Test empty string"""
        assert word_break("", []) is True
    
    def test_empty_dictionary(self):
        """Test with empty dictionary"""
        assert word_break("hello", []) is False
    
    def test_multiple_valid_segmentations(self):
        """Test string with multiple possible segmentations"""
        assert word_break("applepenapple", ["apple", "pen"]) is True
    
    def test_overlapping_words(self):
        """Test with overlapping word patterns"""
        assert word_break("catsandcatsdog", ["cat", "cats", "and", "sand", "dog"]) is True
    
    def test_single_character_match(self):
        """Test single character string that matches"""
        assert word_break("a", ["a"]) is True
    
    def test_single_character_no_match(self):
        """Test single character string that doesn't match"""
        assert word_break("a", ["b"]) is False
    
    def test_long_string_success(self):
        """Test longer string that can be segmented"""
        assert word_break("pineapplepenapple", ["pine", "apple", "pen"]) is True
    
    def test_long_string_failure(self):
        """Test longer string that cannot be segmented"""
        assert word_break("pineapplepenapple", ["pine", "apple"]) is False
    
    def test_repeated_words(self):
        """Test with repeated words in dictionary"""
        assert word_break("aaaa", ["aa", "aaa"]) is True
    
    def test_no_valid_segmentation_exists(self):
        """Test when no valid segmentation exists"""
        assert word_break("abcd", ["ab", "cd", "ef"]) is False
    
    def test_word_dict_as_set(self):
        """Test that function works with word_dict as a set"""
        assert word_break("leetcode", {"leet", "code"}) is True
    
    def test_case_sensitive(self):
        """Test that matching is case-sensitive"""
        assert word_break("Hello", ["hello"]) is False
    
    def test_complex_case(self):
        """Test a more complex case"""
        assert word_break("goalspecial", ["go", "goal", "goals", "special"]) is True
