import pytest
from median_two_sorted import findMedianSortedArrays


class TestMedianTwoSortedArrays:
    """Test cases for finding median of two sorted arrays"""
    
    def test_basic_case_1(self):
        """Test case: [1,3], [2] -> 2.0"""
        assert findMedianSortedArrays([1, 3], [2]) == 2.0
    
    def test_basic_case_2(self):
        """Test case: [1,2], [3,4] -> 2.5"""
        assert findMedianSortedArrays([1, 2], [3, 4]) == 2.5
    
    def test_empty_first_array(self):
        """Test case: [], [1] -> 1.0"""
        assert findMedianSortedArrays([], [1]) == 1.0
    
    def test_empty_second_array(self):
        """Test case: [1], [] -> 1.0"""
        assert findMedianSortedArrays([1], []) == 1.0
    
    def test_single_element_each(self):
        """Test case: [1], [2] -> 1.5"""
        assert findMedianSortedArrays([1], [2]) == 1.5
    
    def test_odd_total_length(self):
        """Test case: [1,3,5], [2,4,6] -> 3.5"""
        result = findMedianSortedArrays([1, 3, 5], [2, 4, 6])
        assert result == 3.5
    
    def test_even_total_length(self):
        """Test case: [1,3], [2] -> 2.0"""
        result = findMedianSortedArrays([1, 3], [2])
        assert result == 2.0
    
    def test_all_first_array_smaller(self):
        """Test case: [1,2,3], [4,5,6] -> 3.5"""
        result = findMedianSortedArrays([1, 2, 3], [4, 5, 6])
        assert result == 3.5
    
    def test_all_second_array_smaller(self):
        """Test case: [4,5,6], [1,2,3] -> 3.5"""
        result = findMedianSortedArrays([4, 5, 6], [1, 2, 3])
        assert result == 3.5
    
    def test_interleaved_arrays(self):
        """Test case: [1,3,5,7], [2,4,6,8] -> 4.5"""
        result = findMedianSortedArrays([1, 3, 5, 7], [2, 4, 6, 8])
        assert result == 4.5
    
    def test_duplicate_elements(self):
        """Test case: [1,1,1], [1,1,1] -> 1.0"""
        result = findMedianSortedArrays([1, 1, 1], [1, 1, 1])
        assert result == 1.0
    
    def test_negative_numbers(self):
        """Test case: [-2,-1], [0,1] -> -0.5"""
        result = findMedianSortedArrays([-2, -1], [0, 1])
        assert result == -0.5
    
    def test_mixed_negative_positive(self):
        """Test case: [-5,-3,-1], [0,2,4] -> -0.5"""
        result = findMedianSortedArrays([-5, -3, -1], [0, 2, 4])
        assert result == -0.5
    
    def test_large_arrays(self):
        """Test case with larger arrays"""
        nums1 = list(range(0, 100, 2))  # [0, 2, 4, ..., 98]
        nums2 = list(range(1, 100, 2))  # [1, 3, 5, ..., 99]
        result = findMedianSortedArrays(nums1, nums2)
        assert result == 49.5
    
    def test_single_element_in_first(self):
        """Test case: [2], [1,3,4,5] -> 3.0"""
        result = findMedianSortedArrays([2], [1, 3, 4, 5])
        assert result == 3.0
    
    def test_single_element_in_second(self):
        """Test case: [1,3,4,5], [2] -> 3.0"""
        result = findMedianSortedArrays([1, 3, 4, 5], [2])
        assert result == 3.0
