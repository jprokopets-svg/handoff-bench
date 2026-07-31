import pytest
from median_two_sorted import findMedianSortedArrays


def test_basic_case_1():
    """Test with two arrays of different sizes"""
    nums1 = [1, 3]
    nums2 = [2]
    assert findMedianSortedArrays(nums1, nums2) == 2.0


def test_basic_case_2():
    """Test with two arrays of different sizes"""
    nums1 = [1, 2]
    nums2 = [3, 4]
    assert findMedianSortedArrays(nums1, nums2) == 2.5


def test_empty_array_1():
    """Test with one empty array"""
    nums1 = []
    nums2 = [1]
    assert findMedianSortedArrays(nums1, nums2) == 1.0


def test_empty_array_2():
    """Test with one empty array"""
    nums1 = [2]
    nums2 = []
    assert findMedianSortedArrays(nums1, nums2) == 2.0


def test_both_empty():
    """Test with both empty arrays"""
    nums1 = []
    nums2 = []
    # This is an edge case - median of empty is undefined
    # but we should handle it gracefully
    result = findMedianSortedArrays(nums1, nums2)
    assert result is not None


def test_single_element_each():
    """Test with single element in each array"""
    nums1 = [1]
    nums2 = [2]
    assert findMedianSortedArrays(nums1, nums2) == 1.5


def test_larger_arrays():
    """Test with larger arrays"""
    nums1 = [1, 3, 5, 7]
    nums2 = [2, 4, 6, 8]
    assert findMedianSortedArrays(nums1, nums2) == 4.5


def test_odd_total_length():
    """Test when total length is odd"""
    nums1 = [1, 3]
    nums2 = [2, 4, 5]
    assert findMedianSortedArrays(nums1, nums2) == 3.0


def test_all_in_first_array():
    """Test when second array is empty"""
    nums1 = [1, 2, 3, 4, 5]
    nums2 = []
    assert findMedianSortedArrays(nums1, nums2) == 3.0


def test_all_in_second_array():
    """Test when first array is empty"""
    nums1 = []
    nums2 = [1, 2, 3, 4, 5]
    assert findMedianSortedArrays(nums1, nums2) == 3.0


def test_negative_numbers():
    """Test with negative numbers"""
    nums1 = [-2, -1]
    nums2 = [0, 1]
    assert findMedianSortedArrays(nums1, nums2) == -0.5


def test_duplicates():
    """Test with duplicate values"""
    nums1 = [1, 1, 1]
    nums2 = [1, 1, 1]
    assert findMedianSortedArrays(nums1, nums2) == 1.0
