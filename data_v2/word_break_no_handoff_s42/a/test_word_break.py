import pytest
from word_break import word_break


def test_word_break_basic():
    """Test basic word break cases"""
    assert word_break("leetcode", ["leet", "code"]) == True
    assert word_break("applepenapple", ["apple", "pen"]) == True
    assert word_break("catsandog", ["cat", "cats", "and", "sand", "dog"]) == False


def test_word_break_empty_string():
    """Test with empty string"""
    assert word_break("", []) == True
    assert word_break("", ["a"]) == True


def test_word_break_single_word():
    """Test with single word"""
    assert word_break("hello", ["hello"]) == True
    assert word_break("hello", ["hell"]) == False


def test_word_break_no_match():
    """Test when no words match"""
    assert word_break("abc", ["def", "ghi"]) == False


def test_word_break_multiple_combinations():
    """Test strings that can be segmented in multiple ways"""
    assert word_break("aaab", ["a", "aa", "aaa", "b"]) == True
    assert word_break("aaab", ["a", "aa", "b"]) == True


def test_word_break_complex():
    """Test more complex cases"""
    assert word_break("cars", ["car", "ca", "rs", "s"]) == True
    assert word_break("cars", ["ca", "rs", "s"]) == False
