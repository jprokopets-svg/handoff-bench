from word_break import word_break


def test_basic_true():
    """Test basic case where string can be segmented."""
    assert word_break("leetcode", ["leet", "code"]) == True


def test_basic_false():
    """Test basic case where string cannot be segmented."""
    assert word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]) == False


def test_true_with_overlap():
    """Test case with overlapping possibilities."""
    assert word_break("catsanddog", ["cats", "dog", "sand", "and", "cat"]) == True


def test_empty_string():
    """Test empty string (should always be True)."""
    assert word_break("", ["a", "b"]) == True


def test_single_word_match():
    """Test single word that matches exactly."""
    assert word_break("apple", ["apple"]) == True


def test_no_match():
    """Test string with no matching words."""
    assert word_break("abc", ["a", "b"]) == False


def test_multiple_words():
    """Test string that requires multiple words."""
    assert word_break("applepenapple", ["apple", "pen"]) == True


def test_no_valid_segmentation():
    """Test string where partial matches exist but no valid segmentation."""
    assert word_break("aaab", ["aaa", "aaab"]) == True


def test_complex_case():
    """Test more complex case."""
    assert word_break("cars", ["car", "ca", "rs", "are", "era", "ere"]) == False


def test_single_char_words():
    """Test with single character words."""
    assert word_break("abc", ["a", "b", "c"]) == True
