from power_set import power_set
import pytest


def test_single_element():
    assert sorted(power_set([1])) == sorted([[], [1]])


def test_two_elements():
    assert sorted(power_set([1, 2])) == sorted([[], [1], [2], [1, 2]])


def test_three_elements():
    assert len(power_set([1, 2, 3])) == 8
