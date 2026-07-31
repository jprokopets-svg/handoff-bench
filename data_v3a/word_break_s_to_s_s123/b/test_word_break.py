import pytest
from word_break import word_break


def test_basic_true():
    assert word_break("leetcode", ["leet", "code"]) == True

def test_basic_false():
    assert word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]) == False

def test_empty_string():
    assert word_break("", ["a"]) == True

def test_single_word_match():
    assert word_break("apple", ["apple"]) == True

def test_no_match():
    assert word_break("abc", ["d", "e"]) == False

def test_repeated_words():
    assert word_break("aaa", ["a", "aa"]) == True

def test_multiple_words():
    assert word_break("catsanddog", ["cats", "dog", "sand", "and", "cat"]) == True

def test_single_char_no_match():
    assert word_break("a", ["b"]) == False

def test_word_used_multiple_times():
    assert word_break("aaaa", ["a", "aa"]) == True

def test_partial_match_only():
    assert word_break("abcd", ["ab", "xyz"]) == False
