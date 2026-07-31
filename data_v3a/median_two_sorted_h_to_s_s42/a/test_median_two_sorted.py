import pytest
from median_two_sorted import findMedianSortedArrays


def test_basic_even_length():
    """Test with two arrays of equal length resulting in even total"""
    assert findMedianSortedArrays([1, 3], [2]) == 2.0


def test_basic_odd_length():
    """Test with arrays resulting in odd total length"""
    assert findMedianSortedArrays([1, 2], [3, 4]) == 2.5


def test_empty_first_array():
    """Test when first array is empty"""
    assert findMedianSortedArrays([], [1]) == 1.0


def test_empty_second_array():
    """Test when second array is empty"""
    assert findMedianSortedArrays([2], []) == 2.0


def test_both_empty():
    """Test when both arrays are empty"""
    result = findMedianSortedArrays([], [])
    assert result is not None


def test_single_elements():
    """Test with single elements in each array"""
    assert findMedianSortedArrays([1], [2]) == 1.5


def test_no_overlap():
    """Test with non-overlapping arrays"""
    assert findMedianSortedArrays([1, 2], [3, 4]) == 2.5


def test_complete_overlap():
    """Test with complete overlap"""
    assert findMedianSortedArrays([1, 2, 3], [1, 2, 3]) == 2.0


def test_larger_arrays():
    """Test with larger arrays"""
    assert findMedianSortedArrays([1, 3, 8, 9, 15], [7, 11, 18, 19, 21, 25]) == 11.0


def test_negative_numbers():
    """Test with negative numbers"""
    assert findMedianSortedArrays([-5, -3, -1], [0, 2, 4]) == -0.5


def test_duplicates():
    """Test with duplicate values"""
    assert findMedianSortedArrays([1, 1, 1], [1, 1, 1]) == 1.0
