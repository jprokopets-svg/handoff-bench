from word_break import word_break

def test_basic_true():
    assert word_break("leetcode", ["leet", "code"]) == True

def test_basic_false():
    assert word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]) == False

def test_true_with_backtracking():
    assert word_break("catsanddog", ["cats", "dog", "sand", "and", "cat"]) == True

def test_empty_string():
    assert word_break("", ["a"]) == True

def test_single_word_match():
    assert word_break("apple", ["apple"]) == True

def test_no_match():
    assert word_break("abc", ["a", "b"]) == False

def test_complex_case():
    assert word_break("applepenapple", ["apple", "pen"]) == True

def test_complex_false():
    assert word_break("codeforces", ["code", "force"]) == False

def test_single_char():
    assert word_break("a", ["a"]) == True

def test_single_char_no_match():
    assert word_break("a", ["b"]) == False
