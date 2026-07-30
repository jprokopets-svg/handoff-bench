import pytest
from median_two_sorted import findMedianSortedArrays


def test_example1():
    """Test case: [1,3] and [2]"""
    assert findMedianSortedArrays([1, 3], [2]) == 2.0


def test_example2():
    """Test case: [1,2] and [3,4]"""
    assert findMedianSortedArrays([1, 2], [3, 4]) == 2.5


def test_empty_first():
    """Test case: [] and [1]"""
    assert findMedianSortedArrays([], [1]) == 1.0


def test_empty_both():
    """Test case: [0,0] and [0,0]"""
    assert findMedianSortedArrays([0, 0], [0, 0]) == 0.0


def test_single_elements():
    """Test case: [1] and [2]"""
    assert findMedianSortedArrays([1], [2]) == 1.5


def test_empty_second():
    """Test case: [1] and []"""
    assert findMedianSortedArrays([1], []) == 1.0


def test_larger_first_array():
    """Test case: [3] and [1,2]"""
    assert findMedianSortedArrays([3], [1, 2]) == 2.0


def test_odd_total_length():
    """Test case: [1,2,3] and [4,5,6]"""
    assert findMedianSortedArrays([1, 2, 3], [4, 5, 6]) == 3.5


def test_all_first_smaller():
    """Test case: [1,2] and [3,4,5,6]"""
    assert findMedianSortedArrays([1, 2], [3, 4, 5, 6]) == 3.5
