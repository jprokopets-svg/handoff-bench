import pytest
from median_two_sorted import findMedianSortedArrays


def test_example1():
    """Test with two arrays of different sizes"""
    nums1 = [1, 3]
    nums2 = [2]
    assert findMedianSortedArrays(nums1, nums2) == 2.0


def test_example2():
    """Test with two arrays of different sizes"""
    nums1 = [1, 2]
    nums2 = [3, 4]
    assert findMedianSortedArrays(nums1, nums2) == 2.5


def test_empty_first():
    """Test with empty first array"""
    nums1 = []
    nums2 = [1]
    assert findMedianSortedArrays(nums1, nums2) == 1.0


def test_empty_second():
    """Test with empty second array"""
    nums1 = [2]
    nums2 = []
    assert findMedianSortedArrays(nums1, nums2) == 2.0


def test_single_elements():
    """Test with single elements in each array"""
    nums1 = [1]
    nums2 = [2]
    assert findMedianSortedArrays(nums1, nums2) == 1.5


def test_larger_arrays():
    """Test with larger arrays"""
    nums1 = [1, 3, 8, 9, 15]
    nums2 = [7, 11, 18, 19, 21, 25]
    assert findMedianSortedArrays(nums1, nums2) == 11.0
