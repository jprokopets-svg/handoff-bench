import pytest
from word_break import word_break

def test_word_break_leetcode():
    assert word_break('leetcode', ['leet','code']) == True

def test_word_break_applepenapple():
    assert word_break('applepenapple', ['apple','pen']) == True

def test_word_break_catsandog():
    assert word_break('catsandog', ['cats','dog','sand','and','cat']) == False

def test_word_break_empty_string():
    assert word_break('', ['a']) == True
