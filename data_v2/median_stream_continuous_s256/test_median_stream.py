from median_stream import *


def test_median_two_elements():
    mf = MedianFinder()
    mf.add_num(1)
    mf.add_num(2)
    assert mf.find_median() == 1.5


def test_median_single_element():
    mf = MedianFinder()
    mf.add_num(1)
    assert mf.find_median() == 1.0


def test_median_three_elements():
    mf = MedianFinder()
    mf.add_num(1)
    mf.add_num(2)
    mf.add_num(3)
    assert mf.find_median() == 2.0
