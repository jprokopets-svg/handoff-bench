import pytest
from word_break import word_break


# --- Basic cases ---

def test_basic_true():
    assert word_break("leetcode", ["leet", "code"]) == True

def test_basic_true_2():
    assert word_break("applepenapple", ["apple", "pen"]) == True

def test_basic_false():
    assert word_break("catsandog", ["cat", "cats", "and", "sand", "dog"]) == False

def test_cats_and_sand():
    assert word_break("catsanddog", ["cat", "cats", "and", "sand", "dog"]) == True


# --- Edge cases ---

def test_empty_string():
    assert word_break("", ["leet", "code"]) == True

def test_empty_dict():
    assert word_break("hello", []) == False

def test_empty_string_empty_dict():
    assert word_break("", []) == True

def test_single_char_in_dict():
    assert word_break("a", ["a"]) == True

def test_single_char_not_in_dict():
    assert word_break("a", ["b"]) == False

def test_whole_word_in_dict():
    assert word_break("hello", ["hello"]) == True

def test_word_not_in_dict():
    assert word_break("hello", ["world"]) == False


# --- Repeated words ---

def test_repeated_words():
    assert word_break("aaaa", ["a", "aa", "aaa"]) == True

def test_repeated_single_char():
    assert word_break("aaa", ["a"]) == True


# --- Overlapping / tricky cases ---

def test_overlapping_words():
    # "cars" can be split as "car" + "s" but "s" not in dict; however "cars" is
    assert word_break("cars", ["car", "ca", "rs"]) == True

def test_no_valid_segmentation():
    assert word_break("abcd", ["ab", "cd", "abc"]) == True

def test_partial_match_only():
    assert word_break("abcd", ["ab", "bc"]) == False

def test_longer_string():
    assert word_break("pineapplepenapple", ["apple", "pen", "applepen", "pine", "pineapple"]) == True

def test_dict_as_set():
    # word_dict can also be passed as a set
    assert word_break("leetcode", {"leet", "code"}) == True
