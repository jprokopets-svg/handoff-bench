import pytest
from median_two_sorted import findMedianSortedArrays


def test_example1():
    """Test case: nums1 = [1,3], nums2 = [2]"""
    assert findMedianSortedArrays([1, 3], [2]) == 2.0


def test_example2():
    """Test case: nums1 = [1,2], nums2 = [3,4]"""
    assert findMedianSortedArrays([1, 2], [3, 4]) == 2.5


def test_empty_first_array():
    """Test case: nums1 = [], nums2 = [1]"""
    assert findMedianSortedArrays([], [1]) == 1.0


def test_empty_second_array():
    """Test case: nums1 = [1], nums2 = []"""
    assert findMedianSortedArrays([1], []) == 1.0


def test_single_elements():
    """Test case: nums1 = [1], nums2 = [2]"""
    assert findMedianSortedArrays([1], [2]) == 1.5


def test_larger_arrays():
    """Test case: nums1 = [1,3,8,9,15], nums2 = [7,11,18,19,21,25]"""
    result = findMedianSortedArrays([1, 3, 8, 9, 15], [7, 11, 18, 19, 21, 25])
    assert result == 11.0


def test_all_first_smaller():
    """Test case: nums1 = [1,2], nums2 = [3,4,5,6]"""
    assert findMedianSortedArrays([1, 2], [3, 4, 5, 6]) == 3.5


def test_all_second_smaller():
    """Test case: nums1 = [3,4,5,6], nums2 = [1,2]"""
    assert findMedianSortedArrays([3, 4, 5, 6], [1, 2]) == 3.5


def test_interleaved():
    """Test case: nums1 = [1,3,5,7], nums2 = [2,4,6,8]"""
    assert findMedianSortedArrays([1, 3, 5, 7], [2, 4, 6, 8]) == 4.5


def test_duplicates():
    """Test case: nums1 = [1,1,1], nums2 = [1,1,1]"""
    assert findMedianSortedArrays([1, 1, 1], [1, 1, 1]) == 1.0
