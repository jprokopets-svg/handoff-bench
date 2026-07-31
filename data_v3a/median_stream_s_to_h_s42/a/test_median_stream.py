import pytest
from median_stream import MedianFinder


# ---------------------------------------------------------------------------
# Basic functionality
# ---------------------------------------------------------------------------

def test_single_element():
    mf = MedianFinder()
    mf.add_num(5)
    assert mf.find_median() == 5.0


def test_two_elements_even_median():
    mf = MedianFinder()
    mf.add_num(1)
    mf.add_num(3)
    assert mf.find_median() == 2.0


def test_three_elements_odd_count():
    mf = MedianFinder()
    mf.add_num(1)
    mf.add_num(2)
    mf.add_num(3)
    assert mf.find_median() == 2.0


def test_median_updates_as_numbers_arrive():
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


# ---------------------------------------------------------------------------
# Order independence
# ---------------------------------------------------------------------------

def test_descending_input():
    mf = MedianFinder()
    for n in [5, 4, 3, 2, 1]:
        mf.add_num(n)
    assert mf.find_median() == 3.0


def test_unsorted_input():
    mf = MedianFinder()
    for n in [3, 1, 4, 1, 5, 9, 2, 6]:
        mf.add_num(n)
    # sorted: [1,1,2,3,4,5,6,9] -> median = (3+4)/2 = 3.5
    assert mf.find_median() == 3.5


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_duplicate_values():
    mf = MedianFinder()
    for n in [2, 2, 2, 2]:
        mf.add_num(n)
    assert mf.find_median() == 2.0


def test_negative_numbers():
    mf = MedianFinder()
    for n in [-5, -3, -1]:
        mf.add_num(n)
    assert mf.find_median() == -3.0


def test_mixed_positive_negative():
    mf = MedianFinder()
    for n in [-10, 0, 10]:
        mf.add_num(n)
    assert mf.find_median() == 0.0


def test_float_inputs():
    mf = MedianFinder()
    mf.add_num(1.5)
    mf.add_num(2.5)
    assert mf.find_median() == 2.0


def test_large_stream():
    mf = MedianFinder()
    for i in range(1, 1001):
        mf.add_num(i)
    # 1..1000 even count: median = (500 + 501) / 2 = 500.5
    assert mf.find_median() == 500.5


def test_empty_raises():
    mf = MedianFinder()
    with pytest.raises((ValueError, IndexError)):
        mf.find_median()


# ---------------------------------------------------------------------------
# Multiple independent instances
# ---------------------------------------------------------------------------

def test_independent_instances():
    mf1 = MedianFinder()
    mf2 = MedianFinder()
    mf1.add_num(10)
    mf2.add_num(1)
    mf2.add_num(2)
    assert mf1.find_median() == 10.0
    assert mf2.find_median() == 1.5
