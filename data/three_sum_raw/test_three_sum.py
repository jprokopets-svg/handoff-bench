from three_sum import *

import pytest


def test_three_sum_basic():
    assert three_sum([-1,0,1,2,-1,-4]) == [[-1,-1,2],[-1,0,1]]

def test_three_sum_no_solution():
    assert three_sum([0,1,1]) == []

def test_three_sum_all_zeros():
    assert three_sum([0,0,0]) == [[0,0,0]]
