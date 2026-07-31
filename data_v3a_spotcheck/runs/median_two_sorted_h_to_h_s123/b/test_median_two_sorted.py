import pytest
from median_two_sorted import findMedianSortedArrays


class TestMedianTwoSortedArrays:
    """Test cases for finding median of two sorted arrays."""
    
    def test_basic_case_1(self):
        """Test basic case: [1,3], [2] -> 2.0"""
        assert findMedianSortedArrays([1, 3], [2]) == 2.0
    
    def test_basic_case_2(self):
        """Test basic case: [1,2], [3,4] -> 2.5"""
        assert findMedianSortedArrays([1, 2], [3, 4]) == 2.5
    
    def test_empty_first_array(self):
        """Test with empty first array: [], [1] -> 1.0"""
        assert findMedianSortedArrays([], [1]) == 1.0
    
    def test_empty_second_array(self):
        """Test with empty second array: [1], [] -> 1.0"""
        assert findMedianSortedArrays([1], []) == 1.0
    
    def test_single_element_each(self):
        """Test with single element in each: [1], [2] -> 1.5"""
        assert findMedianSortedArrays([1], [2]) == 1.5
    
    def test_duplicates(self):
        """Test with duplicates: [1,1], [1,1] -> 1.0"""
        assert findMedianSortedArrays([1, 1], [1, 1]) == 1.0
    
    def test_all_first_array_smaller(self):
        """Test when all elements of first array are smaller"""
        assert findMedianSortedArrays([1, 2], [3, 4, 5]) == 3.0
    
    def test_all_first_array_larger(self):
        """Test when all elements of first array are larger"""
        assert findMedianSortedArrays([4, 5], [1, 2, 3]) == 3.0
    
    def test_interleaved_arrays(self):
        """Test with interleaved arrays: [1,3,5], [2,4,6] -> 3.5"""
        assert findMedianSortedArrays([1, 3, 5], [2, 4, 6]) == 3.5
    
    def test_odd_total_length(self):
        """Test with odd total length"""
        assert findMedianSortedArrays([1, 2, 3], [4, 5]) == 3.0
    
    def test_even_total_length(self):
        """Test with even total length"""
        assert findMedianSortedArrays([1, 2], [3, 4]) == 2.5
    
    def test_large_numbers(self):
        """Test with large numbers"""
        assert findMedianSortedArrays([1000000], [1000001]) == 1000000.5
    
    def test_negative_numbers(self):
        """Test with negative numbers"""
        assert findMedianSortedArrays([-5, -3], [-1, 0, 2]) == -1.0
    
    def test_mixed_positive_negative(self):
        """Test with mixed positive and negative numbers"""
        assert findMedianSortedArrays([-2, 0], [-1, 1]) == -0.5
    
    def test_single_element_in_first(self):
        """Test with single element in first array"""
        assert findMedianSortedArrays([2], [1, 3, 4]) == 2.5
    
    def test_longer_second_array(self):
        """Test with much longer second array"""
        assert findMedianSortedArrays([1], [2, 3, 4, 5, 6, 7, 8]) == 4.5
    
    def test_longer_first_array(self):
        """Test with longer first array (should swap internally)"""
        assert findMedianSortedArrays([1, 2, 3, 4, 5], [3]) == 3.0
    
    def test_identical_arrays(self):
        """Test with identical arrays"""
        assert findMedianSortedArrays([1, 2, 3], [1, 2, 3]) == 2.0
    
    def test_floats(self):
        """Test with floating point numbers"""
        assert findMedianSortedArrays([1.5, 2.5], [2.0, 3.0]) == 2.25
