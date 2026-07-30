from three_sum import three_sum
import pytest


def test_basic_case():
    assert three_sum([-1, 0, 1, 2, -1, -4]) == [[-1, -1, 2], [-1, 0, 1]]


def test_no_solution():
    assert three_sum([0, 1, 1]) == []


def test_all_zeros():
    assert three_sum([0, 0, 0]) == [[0, 0, 0]]
