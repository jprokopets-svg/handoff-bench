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
    mf.add_num(3)
    mf.add_num(2)
    assert mf.find_median() == 2.0


def test_odd_count():
    mf = MedianFinder()
    for n in [5, 3, 8, 1, 9]:
        mf.add_num(n)
    # sorted: [1, 3, 5, 8, 9] -> median = 5
    assert mf.find_median() == 5.0


def test_even_count():
    mf = MedianFinder()
    for n in [5, 3, 8, 1]:
        mf.add_num(n)
    # sorted: [1, 3, 5, 8] -> median = (3+5)/2 = 4.0
    assert mf.find_median() == 4.0


def test_duplicates():
    mf = MedianFinder()
    for n in [2, 2, 2, 2]:
        mf.add_num(n)
    assert mf.find_median() == 2.0


def test_negative_numbers():
    mf = MedianFinder()
    for n in [-5, -1, -3]:
        mf.add_num(n)
    # sorted: [-5, -3, -1] -> median = -3
    assert mf.find_median() == -3.0


def test_mixed_numbers():
    mf = MedianFinder()
    for n in [-10, 0, 10]:
        mf.add_num(n)
    assert mf.find_median() == 0.0


def test_incremental_medians():
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


def test_empty_raises():
    mf = MedianFinder()
    with pytest.raises((ValueError, IndexError)):
        mf.find_median()


def test_large_stream():
    mf = MedianFinder()
    for i in range(1, 1001):
        mf.add_num(i)
    # 1..1000 even count: median = (500+501)/2 = 500.5
    assert mf.find_median() == 500.5
