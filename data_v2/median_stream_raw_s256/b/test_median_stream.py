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
    mf.add_num(2)
    mf.add_num(3)
    assert mf.find_median() == 2.0


def test_even_numbers():
    mf = MedianFinder()
    mf.add_num(1)
    mf.add_num(2)
    mf.add_num(3)
    mf.add_num(4)
    assert mf.find_median() == 2.5


def test_unordered_stream():
    mf = MedianFinder()
    mf.add_num(5)
    assert mf.find_median() == 5.0
    mf.add_num(15)
    assert mf.find_median() == 10.0
    mf.add_num(1)
    assert mf.find_median() == 5.0
    mf.add_num(3)
    assert mf.find_median() == 4.0
    mf.add_num(8)
    assert mf.find_median() == 5.0


def test_negative_numbers():
    mf = MedianFinder()
    mf.add_num(-1)
    mf.add_num(-2)
    mf.add_num(-3)
    assert mf.find_median() == -2.0


def test_mixed_positive_negative():
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
