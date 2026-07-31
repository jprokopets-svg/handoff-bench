import pytest
from median_two_sorted import find_median_sorted_arrays


def test_basic_odd_total():
    assert find_median_sorted_arrays([1, 3], [2]) == 2.0


def test_basic_even_total():
    assert find_median_sorted_arrays([1, 2], [3, 4]) == 2.5


def test_empty_first_array():
    assert find_median_sorted_arrays([], [1]) == 1.0


def test_empty_first_array_even():
    assert find_median_sorted_arrays([], [1, 2]) == 1.5


def test_empty_second_array():
    assert find_median_sorted_arrays([2], []) == 2.0


def test_single_elements():
    assert find_median_sorted_arrays([1], [2]) == 1.5


def test_same_elements():
    assert find_median_sorted_arrays([1, 1], [1, 1]) == 1.0


def test_no_overlap_even():
    assert find_median_sorted_arrays([1, 2], [3, 4]) == 2.5


def test_no_overlap_odd():
    assert find_median_sorted_arrays([1, 2], [3, 4, 5]) == 3.0


def test_larger_arrays():
    assert find_median_sorted_arrays([1, 3, 5, 7], [2, 4, 6, 8]) == 4.5


def test_one_element_arrays():
    assert find_median_sorted_arrays([3], [1, 2, 4, 5]) == 3.0


def test_negative_numbers():
    assert find_median_sorted_arrays([-5, -3, -1], [-4, -2, 0]) == -2.5


def test_mixed_negative_positive():
    assert find_median_sorted_arrays([-3, -1, 2], [-2, 0, 3]) == 0.0 or \
           find_median_sorted_arrays([-3, -1, 2], [-2, 0, 3]) == pytest.approx((-1 + 0) / 2.0)


def test_large_difference():
    assert find_median_sorted_arrays([1, 2], [1000000]) == 2.0


def test_returns_float():
    result = find_median_sorted_arrays([1, 3], [2])
    assert isinstance(result, float)


def test_already_interleaved():
    assert find_median_sorted_arrays([1, 3, 5], [2, 4, 6]) == 3.5
