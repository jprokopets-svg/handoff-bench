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


def test_three_numbers():
    mf = MedianFinder()
    mf.add_num(1)
    mf.add_num(2)
    mf.add_num(3)
    assert mf.find_median() == 2.0


def test_odd_stream():
    mf = MedianFinder()
    for n in [5, 3, 8, 1, 9]:
        mf.add_num(n)
    # sorted: [1, 3, 5, 8, 9] -> median = 5
    assert mf.find_median() == 5.0


def test_even_stream():
    mf = MedianFinder()
    for n in [5, 3, 8, 1]:
        mf.add_num(n)
    # sorted: [1, 3, 5, 8] -> median = (3+5)/2 = 4.0
    assert mf.find_median() == 4.0


def test_negative_numbers():
    mf = MedianFinder()
    mf.add_num(-5)
    mf.add_num(-3)
    mf.add_num(-8)
    # sorted: [-8, -5, -3] -> median = -5
    assert mf.find_median() == -5.0


def test_mixed_positive_negative():
    mf = MedianFinder()
    mf.add_num(-1)
    mf.add_num(0)
    mf.add_num(1)
    assert mf.find_median() == 0.0


def test_duplicate_values():
    mf = MedianFinder()
    mf.add_num(2)
    mf.add_num(2)
    mf.add_num(2)
    assert mf.find_median() == 2.0


def test_duplicate_even():
    mf = MedianFinder()
    mf.add_num(3)
    mf.add_num(3)
    assert mf.find_median() == 3.0


def test_incremental_medians():
    mf = MedianFinder()
    mf.add_num(6)
    assert mf.find_median() == 6.0
    mf.add_num(10)
    assert mf.find_median() == 8.0
    mf.add_num(2)
    assert mf.find_median() == 6.0
    mf.add_num(6)
    assert mf.find_median() == 6.0
    mf.add_num(5)
    assert mf.find_median() == 6.0


def test_large_dataset():
    mf = MedianFinder()
    for i in range(1, 1001):
        mf.add_num(i)
    # 1..1000 even count -> median = (500 + 501) / 2 = 500.5
    assert mf.find_median() == 500.5


def test_all_same():
    mf = MedianFinder()
    for _ in range(10):
        mf.add_num(7)
    assert mf.find_median() == 7.0


def test_two_element_negative():
    mf = MedianFinder()
    mf.add_num(-10)
    mf.add_num(-20)
    # sorted: [-20, -10] -> median = -15.0
    assert mf.find_median() == -15.0


def test_descending_order():
    mf = MedianFinder()
    for n in [9, 7, 5, 3, 1]:
        mf.add_num(n)
    # sorted: [1, 3, 5, 7, 9] -> median = 5
    assert mf.find_median() == 5.0


def test_ascending_order():
    mf = MedianFinder()
    for n in [1, 3, 5, 7, 9]:
        mf.add_num(n)
    assert mf.find_median() == 5.0
