from power_set import *

import pytest


def test_power_set_single():
    assert sorted(power_set([1])) == sorted([[], [1]])

def test_power_set_two():
    assert sorted(power_set([1,2])) == sorted([[], [1], [2], [1,2]])

def test_power_set_three():
    assert len(power_set([1,2,3])) == 8
