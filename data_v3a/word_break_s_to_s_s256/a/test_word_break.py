import pytest
from word_break import word_break


def test_basic_true():
    assert word_break("leetcode", ["leet", "code"]) == True

def test_basic_false():
    assert word_break("applepenapple", ["apple", "pen"]) == True

def test_no_match():
    assert word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]) == False

def test_empty_string():
    assert word_break("", ["cat", "dog"]) == True

def test_single_word_match():
    assert word_break("cat", ["cat"]) == True

def test_single_word_no_match():
    assert word_break("cat", ["dog"]) == False

def test_repeated_words():
    assert word_break("aaaa", ["a", "aa", "aaa"]) == True

def test_full_sentence():
    assert word_break("thequickbrownfox", ["the", "quick", "brown", "fox"]) == True

def test_partial_match_fails():
    assert word_break("abcd", ["ab", "c"]) == False

def test_word_dict_as_set():
    assert word_break("leetcode", {"leet", "code"}) == True

def test_longer_string():
    assert word_break("pineapplepenapple", ["apple", "pen", "applepen", "pine", "pineapple"]) == True
