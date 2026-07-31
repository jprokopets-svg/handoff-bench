import pytest
from median_two_sorted import find_median_sorted_arrays


def test_basic_odd():
    assert find_median_sorted_arrays([1, 3], [2]) == 2.0


def test_basic_even():
    assert find_median_sorted_arrays([1, 2], [3, 4]) == 2.5


def test_one_empty_single():
    assert find_median_sorted_arrays([], [1]) == 1.0


def test_one_empty_multiple():
    assert find_median_sorted_arrays([], [1, 2, 3]) == 2.0


def test_both_single():
    assert find_median_sorted_arrays([1], [2]) == 1.5


def test_larger_arrays():
    assert find_median_sorted_arrays([1, 3, 5], [2, 4, 6]) == 3.5


def test_first_larger_than_second():
    assert find_median_sorted_arrays([5, 6], [1, 2, 3, 4]) == 3.5


def test_all_same():
    assert find_median_sorted_arrays([2, 2], [2, 2]) == 2.0


def test_no_overlap_even():
    assert find_median_sorted_arrays([1, 2], [3, 4]) == 2.5


def test_no_overlap_odd():
    assert find_median_sorted_arrays([1, 2], [3, 4, 5]) == 3.0


def test_single_vs_many():
    assert find_median_sorted_arrays([3], [1, 2, 4, 5]) == 3.0


def test_both_empty_raises():
    with pytest.raises((IndexError, ZeroDivisionError, ValueError)):
        find_median_sorted_arrays([], [])


def test_negative_numbers():
    assert find_median_sorted_arrays([-3, -1], [-2, 0]) == -1.5


def test_mixed_negative_positive():
    assert find_median_sorted_arrays([-5, 3], [1, 4]) == 2.0


def test_large_arrays_even():
    nums1 = list(range(1, 10, 2))   # [1, 3, 5, 7, 9]
    nums2 = list(range(2, 11, 2))   # [2, 4, 6, 8, 10]
    assert find_median_sorted_arrays(nums1, nums2) == 5.5


def test_first_all_smaller():
    assert find_median_sorted_arrays([1, 2, 3], [4, 5, 6]) == 3.5


def test_second_all_smaller():
    assert find_median_sorted_arrays([4, 5, 6], [1, 2, 3]) == 3.5


def test_duplicates_across_arrays():
    assert find_median_sorted_arrays([1, 2], [2, 3]) == 2.0


def test_single_element_each():
    assert find_median_sorted_arrays([5], [5]) == 5.0
