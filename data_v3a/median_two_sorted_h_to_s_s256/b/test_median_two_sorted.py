import pytest
from median_two_sorted import findMedianSortedArrays


def test_basic_odd():
    assert findMedianSortedArrays([1, 3], [2]) == 2.0

def test_basic_even():
    assert findMedianSortedArrays([1, 2], [3, 4]) == 2.5

def test_one_empty():
    assert findMedianSortedArrays([], [1]) == 1.0

def test_one_empty_multiple():
    assert findMedianSortedArrays([], [1, 2, 3]) == 2.0

def test_both_single():
    assert findMedianSortedArrays([1], [2]) == 1.5

def test_same_elements():
    assert findMedianSortedArrays([1, 1], [1, 1]) == 1.0

def test_no_overlap_even():
    assert findMedianSortedArrays([1, 2], [5, 6]) == 3.5

def test_no_overlap_odd():
    assert findMedianSortedArrays([1, 2], [5, 6, 7]) == 5.0

def test_larger_arrays():
    assert findMedianSortedArrays([1, 3, 5, 7], [2, 4, 6, 8]) == 4.5

def test_first_larger_than_second():
    assert findMedianSortedArrays([3, 4], [1, 2]) == 2.5

def test_single_element_each():
    assert findMedianSortedArrays([3], [1]) == 2.0

def test_empty_both_single():
    assert findMedianSortedArrays([], [2, 3]) == 2.5

def test_negative_numbers():
    assert findMedianSortedArrays([-3, -1], [-2, 0]) == -1.5

def test_mixed_negative_positive():
    assert findMedianSortedArrays([-5, 3], [-2, 4]) == 0.5

def test_large_difference():
    assert findMedianSortedArrays([1], [1000000]) == 500000.5
