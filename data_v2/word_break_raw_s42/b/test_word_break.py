import pytest
from word_break import word_break


def test_basic_word_break():
    """Test basic word break cases"""
    assert word_break("leetcode", ["leet", "code"]) == True
    assert word_break("applepenapple", ["apple", "pen"]) == True
    assert word_break("catsandsanddog", ["cat", "cats", "and", "sand", "dog"]) == False


def test_empty_string():
    """Test empty string"""
    assert word_break("", []) == True
    assert word_break("", ["word"]) == True


def test_single_word():
    """Test single word cases"""
    assert word_break("hello", ["hello"]) == True
    assert word_break("hello", ["world"]) == False


def test_multiple_combinations():
    """Test cases with multiple possible combinations"""
    assert word_break("aaab", ["a", "aa", "aaa", "b"]) == True
    assert word_break("aaab", ["a", "aa", "b"]) == True


def test_no_valid_segmentation():
    """Test cases where no valid segmentation exists"""
    assert word_break("abc", ["a", "b"]) == False
    assert word_break("abcd", ["a", "b", "c"]) == False


def test_overlapping_words():
    """Test with overlapping word patterns"""
    assert word_break("aaaa", ["aa", "aaa"]) == True
    assert word_break("aaaa", ["aaa"]) == False


def test_case_sensitivity():
    """Test that matching is case sensitive"""
    assert word_break("Hello", ["hello"]) == False
    assert word_break("Hello", ["Hello"]) == True
