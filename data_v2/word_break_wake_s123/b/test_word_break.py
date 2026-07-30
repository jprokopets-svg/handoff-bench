import pytest
from word_break import word_break


class TestWordBreak:
    """Test cases for the word_break function."""
    
    def test_basic_true_case(self):
        """Test a basic case where segmentation is possible."""
        assert word_break("leetcode", ["leet", "code"]) == True
    
    def test_basic_true_case_2(self):
        """Test another basic case where segmentation is possible."""
        assert word_break("applepenapple", ["apple", "pen"]) == True
    
    def test_basic_false_case(self):
        """Test a basic case where segmentation is not possible."""
        assert word_break("catsandog", ["cat", "cats", "and", "sand", "dog"]) == False
    
    def test_empty_string(self):
        """Test with an empty string."""
        assert word_break("", []) == True
    
    def test_empty_string_with_dict(self):
        """Test with an empty string and non-empty dictionary."""
        assert word_break("", ["a", "b"]) == True
    
    def test_single_character_match(self):
        """Test with a single character that matches."""
        assert word_break("a", ["a"]) == True
    
    def test_single_character_no_match(self):
        """Test with a single character that doesn't match."""
        assert word_break("a", ["b"]) == False
    
    def test_word_not_in_dict(self):
        """Test when the entire string is not in the dictionary."""
        assert word_break("hello", ["world"]) == False
    
    def test_overlapping_words(self):
        """Test with overlapping word possibilities."""
        assert word_break("catsandcatsdog", ["cat", "cats", "and", "sand", "dog"]) == True
    
    def test_multiple_segmentations(self):
        """Test a string that can be segmented in multiple ways."""
        assert word_break("aaab", ["a", "aa", "aaa", "b"]) == True
    
    def test_false_with_similar_words(self):
        """Test a case that looks like it could work but doesn't."""
        assert word_break("aaab", ["a", "aa", "aaa"]) == False
    
    def test_long_string(self):
        """Test with a longer string."""
        assert word_break("abcdefghij", ["ab", "cd", "ef", "gh", "ij"]) == True
    
    def test_long_string_false(self):
        """Test with a longer string that cannot be segmented."""
        assert word_break("abcdefghij", ["ab", "cd", "ef", "gh"]) == False
    
    def test_repeated_pattern(self):
        """Test with repeated patterns."""
        assert word_break("aaaa", ["a", "aa"]) == True
    
    def test_word_dict_as_set(self):
        """Test that word_dict can be a set."""
        assert word_break("leetcode", {"leet", "code"}) == True
    
    def test_case_sensitive(self):
        """Test that matching is case-sensitive."""
        assert word_break("LeetCode", ["leet", "code"]) == False
