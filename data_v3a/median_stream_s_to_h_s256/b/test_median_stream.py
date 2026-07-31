import pytest
from median_stream import MedianFinder


def test_single_element():
    mf = MedianFinder()
    mf.add_num(5)
    assert mf.find_median() == 5.0


def test_two_elements():
    mf = MedianFinder()
    mf.add_num(1)
    mf.add_num(3)
    assert mf.find_median() == 2.0


def test_three_elements():
    mf = MedianFinder()
    mf.add_num(1)
    mf.add_num(2)
    mf.add_num(3)
    assert mf.find_median() == 2.0


def test_odd_count():
    mf = MedianFinder()
    for n in [5, 3, 8, 1, 9]:
        mf.add_num(n)
    # sorted: [1, 3, 5, 8, 9] -> median = 5
    assert mf.find_median() == 5.0


def test_even_count():
    mf = MedianFinder()
    for n in [2, 4, 6, 8]:
        mf.add_num(n)
    # sorted: [2, 4, 6, 8] -> median = (4+6)/2 = 5.0
    assert mf.find_median() == 5.0


def test_median_after_each_insertion():
    mf = MedianFinder()
    mf.add_num(1)
    assert mf.find_median() == 1.0
    mf.add_num(2)
    assert mf.find_median() == 1.5
    mf.add_num(3)
    assert mf.find_median() == 2.0
    mf.add_num(4)
    assert mf.find_median() == 2.5
    mf.add_num(5)
    assert mf.find_median() == 3.0


def test_duplicates():
    mf = MedianFinder()
    mf.add_num(3)
    mf.add_num(3)
    mf.add_num(3)
    assert mf.find_median() == 3.0


def test_negative_numbers():
    mf = MedianFinder()
    for n in [-5, -1, -3]:
        mf.add_num(n)
    # sorted: [-5, -3, -1] -> median = -3
    assert mf.find_median() == -3.0


def test_mixed_positive_negative():
    mf = MedianFinder()
    for n in [-10, 5, 0, -3, 7]:
        mf.add_num(n)
    # sorted: [-10, -3, 0, 5, 7] -> median = 0
    assert mf.find_median() == 0.0


def test_large_stream():
    mf = MedianFinder()
    numbers = list(range(1, 101))  # 1 to 100
    for n in numbers:
        mf.add_num(n)
    # Even count: median = (50 + 51) / 2 = 50.5
    assert mf.find_median() == 50.5


def test_reverse_order():
    mf = MedianFinder()
    for n in [9, 7, 5, 3, 1]:
        mf.add_num(n)
    # sorted: [1, 3, 5, 7, 9] -> median = 5
    assert mf.find_median() == 5.0


def test_empty_raises():
    mf = MedianFinder()
    with pytest.raises((ValueError, IndexError)):
        mf.find_median()


def test_float_numbers():
    mf = MedianFinder()
    mf.add_num(1.5)
    mf.add_num(2.5)
    mf.add_num(3.5)
    assert mf.find_median() == 2.5
