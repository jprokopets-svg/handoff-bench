import pytest
from word_break import word_break


def test_basic_true():
    assert word_break("leetcode", ["leet", "code"]) == True

def test_basic_false():
    assert word_break("catsandog", ["cat", "cats", "and", "sand", "dog"]) == False

def test_cats_and_sand():
    assert word_break("catsanddog", ["cat", "cats", "and", "sand", "dog"]) == True

def test_empty_string():
    assert word_break("", ["cat", "dog"]) == True

def test_empty_dict():
    assert word_break("cat", []) == False

def test_empty_string_empty_dict():
    assert word_break("", []) == True

def test_single_word_match():
    assert word_break("apple", ["apple"]) == True

def test_single_word_no_match():
    assert word_break("apple", ["app"]) == False

def test_single_char_match():
    assert word_break("a", ["a"]) == True

def test_single_char_no_match():
    assert word_break("a", ["b"]) == False

def test_overlapping_words():
    # Requires trying "a" + "aa" + "aaa" etc.
    assert word_break("aaaaaaa", ["aaaa", "aaa"]) == True

def test_overlapping_words_false():
    assert word_break("aaaaaab", ["aa", "aaa"]) == False

def test_repeated_word():
    assert word_break("appleapple", ["apple"]) == True

def test_complex_overlap():
    # "pineapplepenapple" -> "pine" + "apple" + "pen" + "apple"
    assert word_break("pineapplepenapple", ["apple", "pen", "applepen", "pine", "pineapple"]) == True

def test_word_dict_as_set():
    # word_dict can also be passed as a set
    assert word_break("leetcode", {"leet", "code"}) == True

def test_no_segmentation_possible():
    assert word_break("abcdef", ["ab", "cd"]) == False

def test_full_string_is_word():
    assert word_break("hello", ["hello", "world"]) == True
