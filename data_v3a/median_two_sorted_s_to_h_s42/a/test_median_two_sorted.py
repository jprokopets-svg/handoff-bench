import pytest
from median_two_sorted import find_median_sorted_arrays


def test_basic_odd_total():
    assert find_median_sorted_arrays([1, 3], [2]) == 2.0


def test_basic_even_total():
    assert find_median_sorted_arrays([1, 2], [3, 4]) == 2.5


def test_empty_first_array():
    assert find_median_sorted_arrays([], [1]) == 1.0


def test_empty_first_array_two_elements():
    assert find_median_sorted_arrays([], [1, 2]) == 1.5


def test_single_elements_equal():
    assert find_median_sorted_arrays([1], [1]) == 1.0


def test_single_elements_different():
    assert find_median_sorted_arrays([1], [2]) == 1.5


def test_disjoint_arrays():
    assert find_median_sorted_arrays([1, 2], [3, 4, 5]) == 3.0


def test_overlapping_arrays():
    assert find_median_sorted_arrays([1, 4, 7], [2, 3, 6]) == 3.5


def test_one_element_each():
    assert find_median_sorted_arrays([3], [4]) == 3.5


def test_larger_arrays():
    assert find_median_sorted_arrays([1, 3, 5, 7], [2, 4, 6, 8]) == 4.5


def test_first_array_larger():
    # nums1 is larger than nums2 — tests the swap logic
    assert find_median_sorted_arrays([1, 2, 3, 4, 5], [6]) == 3.5


def test_negative_numbers():
    assert find_median_sorted_arrays([-5, -3, -1], [-4, -2, 0]) == -2.5


def test_all_same_elements():
    assert find_median_sorted_arrays([2, 2, 2], [2, 2, 2]) == 2.0


def test_empty_second_array():
    assert find_median_sorted_arrays([1, 2, 3], []) == 2.0


def test_both_single_elements():
    assert find_median_sorted_arrays([5], [5]) == 5.0
