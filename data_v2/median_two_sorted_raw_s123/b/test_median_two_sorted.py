import pytest
from median_two_sorted import findMedianSortedArrays


def test_example1():
    """Test case: nums1 = [1,3], nums2 = [2]"""
    assert findMedianSortedArrays([1, 3], [2]) == 2.0


def test_example2():
    """Test case: nums1 = [1,2], nums2 = [3,4]"""
    assert findMedianSortedArrays([1, 2], [3, 4]) == 2.5


def test_empty_first():
    """Test case: nums1 is empty"""
    assert findMedianSortedArrays([], [1]) == 1.0


def test_empty_second():
    """Test case: nums2 is empty"""
    assert findMedianSortedArrays([2], []) == 2.0


def test_single_elements():
    """Test case: single element in each array"""
    assert findMedianSortedArrays([1], [2]) == 1.5


def test_same_elements():
    """Test case: arrays with same elements"""
    assert findMedianSortedArrays([1, 1], [1, 1]) == 1.0


def test_large_arrays():
    """Test case: larger arrays"""
    assert findMedianSortedArrays([1, 3, 5, 7], [2, 4, 6, 8]) == 4.5


def test_negative_numbers():
    """Test case: arrays with negative numbers"""
    assert findMedianSortedArrays([-2, -1], [0, 1]) == -0.5
