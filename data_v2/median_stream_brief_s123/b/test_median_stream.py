import pytest
from median_stream import MedianFinder


def test_single_number():
    mf = MedianFinder()
    mf.add_num(1)
    assert mf.find_median() == 1.0


def test_two_numbers():
    mf = MedianFinder()
    mf.add_num(1)
    mf.add_num(2)
    assert mf.find_median() == 1.5


def test_odd_numbers():
    mf = MedianFinder()
    mf.add_num(1)
    assert mf.find_median() == 1.0
    mf.add_num(2)
    assert mf.find_median() == 1.5
    mf.add_num(3)
    assert mf.find_median() == 2.0


def test_even_numbers():
    mf = MedianFinder()
    mf.add_num(1)
    mf.add_num(2)
    mf.add_num(3)
    mf.add_num(4)
    assert mf.find_median() == 2.5


def test_negative_numbers():
    mf = MedianFinder()
    mf.add_num(-1)
    mf.add_num(0)
    mf.add_num(1)
    assert mf.find_median() == 0.0


def test_duplicates():
    mf = MedianFinder()
    mf.add_num(1)
    mf.add_num(1)
    mf.add_num(1)
    assert mf.find_median() == 1.0


def test_large_stream():
    mf = MedianFinder()
    nums = [5, 15, 1, 3, 8]
    for num in nums:
        mf.add_num(num)
    # Sorted: [1, 3, 5, 8, 15], median is 5
    assert mf.find_median() == 5.0


def test_unsorted_stream():
    mf = MedianFinder()
    nums = [12, 4, 5, 3, 8, 7]
    for num in nums:
        mf.add_num(num)
    # Sorted: [3, 4, 5, 7, 8, 12], median is (5 + 7) / 2 = 6.0
    assert mf.find_median() == 6.0
