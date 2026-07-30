import pytest
from median_stream import MedianFinder


def test_single_number():
    """Test with a single number"""
    mf = MedianFinder()
    mf.add_num(1)
    assert mf.find_median() == 1.0


def test_two_numbers():
    """Test with two numbers"""
    mf = MedianFinder()
    mf.add_num(1)
    mf.add_num(2)
    assert mf.find_median() == 1.5


def test_odd_count():
    """Test with odd number of elements"""
    mf = MedianFinder()
    mf.add_num(1)
    mf.add_num(2)
    mf.add_num(3)
    assert mf.find_median() == 2.0


def test_even_count():
    """Test with even number of elements"""
    mf = MedianFinder()
    mf.add_num(1)
    mf.add_num(2)
    mf.add_num(3)
    mf.add_num(4)
    assert mf.find_median() == 2.5


def test_unordered_stream():
    """Test with unordered stream"""
    mf = MedianFinder()
    mf.add_num(5)
    assert mf.find_median() == 5.0
    mf.add_num(15)
    assert mf.find_median() == 10.0
    mf.add_num(1)
    assert mf.find_median() == 5.0
    mf.add_num(3)
    assert mf.find_median() == 4.0


def test_negative_numbers():
    """Test with negative numbers"""
    mf = MedianFinder()
    mf.add_num(-1)
    mf.add_num(-2)
    mf.add_num(-3)
    assert mf.find_median() == -2.0


def test_mixed_positive_negative():
    """Test with mixed positive and negative numbers"""
    mf = MedianFinder()
    mf.add_num(-1)
    mf.add_num(1)
    assert mf.find_median() == 0.0
    mf.add_num(2)
    assert mf.find_median() == 1.0


def test_duplicates():
    """Test with duplicate numbers"""
    mf = MedianFinder()
    mf.add_num(1)
    mf.add_num(1)
    mf.add_num(1)
    assert mf.find_median() == 1.0


def test_large_stream():
    """Test with a larger stream"""
    mf = MedianFinder()
    nums = [12, 4, 5, 3, 8, 7]
    for num in nums:
        mf.add_num(num)
    # Sorted: [3, 4, 5, 7, 8, 12]
    # Median of 6 elements: (5 + 7) / 2 = 6.0
    assert mf.find_median() == 6.0


def test_zeros():
    """Test with zeros"""
    mf = MedianFinder()
    mf.add_num(0)
    assert mf.find_median() == 0.0
    mf.add_num(0)
    assert mf.find_median() == 0.0
    mf.add_num(1)
    assert mf.find_median() == 0.0
