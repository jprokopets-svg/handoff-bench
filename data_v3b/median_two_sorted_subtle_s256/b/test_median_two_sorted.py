import pytest
from median_two_sorted import findMedianSortedArrays


class TestMedianTwoSortedArrays:
    """Test cases for finding median of two sorted arrays"""
    
    def test_basic_case_1(self):
        """Test case: [1,3] and [2] -> 2.0"""
        assert findMedianSortedArrays([1, 3], [2]) == 2.0
    
    def test_basic_case_2(self):
        """Test case: [1,2] and [3,4] -> 2.5"""
        assert findMedianSortedArrays([1, 2], [3, 4]) == 2.5
    
    def test_empty_first_array(self):
        """Test case: [] and [1] -> 1.0"""
        assert findMedianSortedArrays([], [1]) == 1.0
    
    def test_empty_second_array(self):
        """Test case: [2] and [] -> 2.0"""
        assert findMedianSortedArrays([2], []) == 2.0
    
    def test_single_elements(self):
        """Test case: [1] and [2] -> 1.5"""
        assert findMedianSortedArrays([1], [2]) == 1.5
    
    def test_all_same_elements(self):
        """Test case: [0,0] and [0,0] -> 0.0"""
        assert findMedianSortedArrays([0, 0], [0, 0]) == 0.0
    
    def test_longer_first_array(self):
        """Test case: [1,2,3,4,5] and [6] -> 3.5"""
        assert findMedianSortedArrays([1, 2, 3, 4, 5], [6]) == 3.5
    
    def test_longer_second_array(self):
        """Test case: [1] and [2,3,4,5,6] -> 3.5"""
        assert findMedianSortedArrays([1], [2, 3, 4, 5, 6]) == 3.5
    
    def test_negative_numbers(self):
        """Test case: [-2, -1] and [0, 1] -> -0.5"""
        assert findMedianSortedArrays([-2, -1], [0, 1]) == -0.5
    
    def test_mixed_positive_negative(self):
        """Test case: [-5, -3, -1] and [0, 2, 4] -> -0.5"""
        assert findMedianSortedArrays([-5, -3, -1], [0, 2, 4]) == -0.5
    
    def test_large_arrays(self):
        """Test case with larger arrays"""
        nums1 = list(range(0, 100, 2))  # [0, 2, 4, ..., 98]
        nums2 = list(range(1, 100, 2))  # [1, 3, 5, ..., 99]
        assert findMedianSortedArrays(nums1, nums2) == 49.5
    
    def test_no_overlap(self):
        """Test case: [1, 2] and [3, 4, 5, 6] -> 3.5"""
        assert findMedianSortedArrays([1, 2], [3, 4, 5, 6]) == 3.5
    
    def test_complete_overlap(self):
        """Test case: [1, 2, 3] and [1, 2, 3] -> 2.0"""
        assert findMedianSortedArrays([1, 2, 3], [1, 2, 3]) == 2.0
