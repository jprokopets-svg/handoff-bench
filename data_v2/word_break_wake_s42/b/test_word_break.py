import pytest
from word_break import word_break


def test_basic_case():
    """Test basic word break case"""
    s = "leetcode"
    word_dict = ["leet", "code"]
    assert word_break(s, word_dict) == True


def test_cannot_break():
    """Test case where string cannot be broken"""
    s = "applepenapple"
    word_dict = ["apple", "pen"]
    assert word_break(s, word_dict) == True


def test_cannot_segment():
    """Test case where string cannot be segmented"""
    s = "catsandog"
    word_dict = ["cat", "cats", "and", "sand", "dog"]
    assert word_break(s, word_dict) == False


def test_empty_string():
    """Test empty string"""
    s = ""
    word_dict = ["a", "b"]
    assert word_break(s, word_dict) == True


def test_single_word():
    """Test single word"""
    s = "a"
    word_dict = ["a"]
    assert word_break(s, word_dict) == True


def test_word_not_in_dict():
    """Test word not in dictionary"""
    s = "b"
    word_dict = ["a"]
    assert word_break(s, word_dict) == False


def test_complex_case():
    """Test complex case"""
    s = "aaaaaab"
    word_dict = ["aaaa", "aaa", "aa", "a"]
    assert word_break(s, word_dict) == False


def test_overlapping_words():
    """Test with overlapping word possibilities"""
    s = "abcd"
    word_dict = ["ab", "abc", "cd", "def", "abcd"]
    assert word_break(s, word_dict) == True
