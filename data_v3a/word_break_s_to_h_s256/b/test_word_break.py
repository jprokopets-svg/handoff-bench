from word_break import word_break

def test_basic_true():
    assert word_break("leetcode", ["leet", "code"]) == True

def test_basic_false():
    assert word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]) == False

def test_single_word():
    assert word_break("apple", ["apple"]) == True

def test_empty_string():
    assert word_break("", ["apple"]) == True

def test_no_match():
    assert word_break("abc", ["def", "ghi"]) == False

def test_repeated_words():
    assert word_break("appleapple", ["apple"]) == True

def test_overlapping_words():
    assert word_break("catsanddog", ["cat", "cats", "and", "sand", "dog"]) == True

def test_single_char():
    assert word_break("a", ["a"]) == True

def test_single_char_no_match():
    assert word_break("a", ["b"]) == False

def test_complex_case():
    assert word_break("pineapplepenapple", ["pine", "pineapple", "pen", "apple", "penapple"]) == True

def test_no_solution_with_partial_match():
    assert word_break("aaab", ["aaa", "aaaa", "baa", "baab", "b", "ba"]) == False
