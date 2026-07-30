from median_two_sorted import *


def test_case_1():
    assert find_median_sorted_arrays([1,3], [2]) == 2.0

def test_case_2():
    assert find_median_sorted_arrays([1,2], [3,4]) == 2.5

def test_case_3():
    assert find_median_sorted_arrays([0,0], [0,0]) == 0.0

def test_case_4():
    assert find_median_sorted_arrays([], [1]) == 1.0
