import pytest
from word_break import word_break


def test_word_break_basic():
    """Test basic word break cases"""
    assert word_break("leetcode", ["leet", "code"]) == True
    assert word_break("applepenapple", ["apple", "pen"]) == True
    assert word_break("catsandog", ["cat", "cats", "and", "sand", "dog"]) == False


def test_word_break_empty():
    """Test empty string"""
    assert word_break("", []) == True
    assert word_break("", ["a"]) == True


def test_word_break_single_word():
    """Test single word cases"""
    assert word_break("a", ["a"]) == True
    assert word_break("a", ["b"]) == False


def test_word_break_complex():
    """Test more complex cases"""
    assert word_break("aaaaaab", ["a", "aa", "aaa"]) == False
    assert word_break("aaaaaaa", ["a", "aa", "aaa"]) == True
    assert word_break("abcd", ["ab", "cd"]) == True
    assert word_break("abcd", ["a", "b", "c", "d"]) == True
