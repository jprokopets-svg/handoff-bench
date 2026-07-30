import pytest
from median_two_sorted import findMedianSortedArrays


def test_example1():
    """Test case: [1,3] and [2]"""
    assert findMedianSortedArrays([1, 3], [2]) == 2.0


def test_example2():
    """Test case: [1,2] and [3,4]"""
    assert findMedianSortedArrays([1, 2], [3, 4]) == 2.5


def test_empty_first_array():
    """Test case: [] and [1]"""
    assert findMedianSortedArrays([], [1]) == 1.0


def test_empty_second_array():
    """Test case: [1] and []"""
    assert findMedianSortedArrays([1], []) == 1.0


def test_single_element_each():
    """Test case: [1] and [2]"""
    assert findMedianSortedArrays([1], [2]) == 1.5


def test_larger_first_array():
    """Test case: [1,2,3,4,5] and [6,7,8,9,10]"""
    assert findMedianSortedArrays([1, 2, 3, 4, 5], [6, 7, 8, 9, 10]) == 5.5


def test_overlapping_arrays():
    """Test case: [1,3,5,7] and [2,4,6,8]"""
    assert findMedianSortedArrays([1, 3, 5, 7], [2, 4, 6, 8]) == 4.5


def test_duplicate_elements():
    """Test case: [1,1,1] and [1,1,1]"""
    assert findMedianSortedArrays([1, 1, 1], [1, 1, 1]) == 1.0


def test_negative_numbers():
    """Test case: [-5,-3,-1] and [-4,-2,0]"""
    assert findMedianSortedArrays([-5, -3, -1], [-4, -2, 0]) == -2.5


def test_mixed_positive_negative():
    """Test case: [-2,0,2] and [-1,1,3]"""
    assert findMedianSortedArrays([-2, 0, 2], [-1, 1, 3]) == 0.5
