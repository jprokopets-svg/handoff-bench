import pytest
from median_two_sorted import findMedianSortedArrays


class TestMedianTwoSortedArrays:
    """Test cases for finding median of two sorted arrays."""
    
    def test_example1(self):
        """Test case: [1,3] and [2] -> median = 2.0"""
        nums1 = [1, 3]
        nums2 = [2]
        assert findMedianSortedArrays(nums1, nums2) == 2.0
    
    def test_example2(self):
        """Test case: [1,2] and [3,4] -> median = 2.5"""
        nums1 = [1, 2]
        nums2 = [3, 4]
        assert findMedianSortedArrays(nums1, nums2) == 2.5
    
    def test_single_element_arrays(self):
        """Test case: [1] and [2] -> median = 1.5"""
        nums1 = [1]
        nums2 = [2]
        assert findMedianSortedArrays(nums1, nums2) == 1.5
    
    def test_empty_first_array(self):
        """Test case: [] and [1] -> median = 1.0"""
        nums1 = []
        nums2 = [1]
        assert findMedianSortedArrays(nums1, nums2) == 1.0
    
    def test_empty_second_array(self):
        """Test case: [1] and [] -> median = 1.0"""
        nums1 = [1]
        nums2 = []
        assert findMedianSortedArrays(nums1, nums2) == 1.0
    
    def test_empty_both_arrays(self):
        """Test case: [] and [] -> should handle gracefully"""
        nums1 = []
        nums2 = []
        # This is an edge case - median of empty arrays is undefined
        # The function should return something reasonable
        result = findMedianSortedArrays(nums1, nums2)
        assert isinstance(result, float)
    
    def test_no_overlap(self):
        """Test case: [1,2] and [3,4,5] -> median = 3.0"""
        nums1 = [1, 2]
        nums2 = [3, 4, 5]
        assert findMedianSortedArrays(nums1, nums2) == 3.0
    
    def test_complete_overlap(self):
        """Test case: [1,2,3] and [1,2,3] -> median = 2.0"""
        nums1 = [1, 2, 3]
        nums2 = [1, 2, 3]
        assert findMedianSortedArrays(nums1, nums2) == 2.0
    
    def test_odd_total_length(self):
        """Test case: [1,3,5] and [2,4] -> median = 3.0"""
        nums1 = [1, 3, 5]
        nums2 = [2, 4]
        assert findMedianSortedArrays(nums1, nums2) == 3.0
    
    def test_even_total_length(self):
        """Test case: [1,3] and [2] -> median = 2.0"""
        nums1 = [1, 3]
        nums2 = [2]
        assert findMedianSortedArrays(nums1, nums2) == 2.0
    
    def test_larger_first_array(self):
        """Test case where first array is larger (should be swapped internally)"""
        nums1 = [3, 4, 5]
        nums2 = [1, 2]
        assert findMedianSortedArrays(nums1, nums2) == 3.0
    
    def test_negative_numbers(self):
        """Test case with negative numbers: [-2, -1] and [0, 1] -> median = -0.5"""
        nums1 = [-2, -1]
        nums2 = [0, 1]
        assert findMedianSortedArrays(nums1, nums2) == -0.5
    
    def test_mixed_positive_negative(self):
        """Test case with mixed positive and negative: [-1, 2] and [1, 3] -> median = 1.5"""
        nums1 = [-1, 2]
        nums2 = [1, 3]
        assert findMedianSortedArrays(nums1, nums2) == 1.5
    
    def test_large_arrays(self):
        """Test case with larger arrays"""
        nums1 = [1, 3, 5, 7, 9]
        nums2 = [2, 4, 6, 8, 10]
        assert findMedianSortedArrays(nums1, nums2) == 5.5
    
    def test_duplicate_elements(self):
        """Test case with duplicate elements: [1, 1, 1] and [1, 1, 1] -> median = 1.0"""
        nums1 = [1, 1, 1]
        nums2 = [1, 1, 1]
        assert findMedianSortedArrays(nums1, nums2) == 1.0
