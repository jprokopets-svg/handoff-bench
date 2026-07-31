import pytest
from word_break import word_break


def test_word_break_basic():
    """Test basic word break cases"""
    assert word_break("leetcode", ["leet", "code"]) == True
    assert word_break("applepenapple", ["apple", "pen"]) == True
    assert word_break("catsandog", ["cat", "cats", "and", "sand", "dog"]) == False


def test_word_break_empty():
    """Test empty string"""
    assert word_break("", ["a", "b"]) == True


def test_word_break_single_word():
    """Test single word"""
    assert word_break("hello", ["hello"]) == True
    assert word_break("hello", ["world"]) == False


def test_word_break_no_match():
    """Test when no words match"""
    assert word_break("abc", ["def", "ghi"]) == False


def test_word_break_overlapping():
    """Test overlapping word possibilities"""
    assert word_break("aaab", ["a", "aa", "aaa", "aaaa", "aaaab"]) == True
    assert word_break("aaab", ["a", "aa", "aaa", "aaaa"]) == False
