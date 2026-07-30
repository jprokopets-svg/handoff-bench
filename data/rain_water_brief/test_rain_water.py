from rain_water import trap
import pytest


def test_basic_example():
    assert trap([0,1,0,2,1,0,1,3,2,1,2,1]) == 6


def test_example_2():
    assert trap([4,2,0,3,2,5]) == 9


def test_simple_valley():
    assert trap([1,0,1]) == 1
