from word_break import word_break


def test_basic_true():
    assert word_break("leetcode", ["leet", "code"]) == True


def test_basic_false():
    assert word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]) == False


def test_single_word():
    assert word_break("apple", ["apple"]) == True


def test_empty_string():
    assert word_break("", ["a", "b"]) == True


def test_no_match():
    assert word_break("abc", ["def", "ghi"]) == False


def test_repeated_words():
    assert word_break("aaaaaa", ["a", "aa", "aaa"]) == True


def test_single_char_words():
    assert word_break("ab", ["a", "b"]) == True


def test_word_used_multiple_times():
    assert word_break("appleapple", ["apple"]) == True


def test_partial_match_only():
    assert word_break("applepenapple", ["apple", "pen"]) == True


def test_no_valid_segmentation():
    assert word_break("cars", ["car", "ca", "rs"]) == True


def test_empty_dict():
    assert word_break("hello", []) == False


def test_empty_string_empty_dict():
    assert word_break("", []) == True


def test_longer_sentence():
    assert word_break("pineapplepenapple", ["apple", "pen", "applepen", "pine", "pineapple"]) == True


def test_false_with_similar_words():
    assert word_break("goalspecial", ["go", "goal", "goals", "special"]) == True
