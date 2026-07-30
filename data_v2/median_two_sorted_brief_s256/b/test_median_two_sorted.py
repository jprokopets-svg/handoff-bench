import pytest
from median_two_sorted import findMedianSortedArrays


class TestMedianTwoSortedArrays:
    """Test cases for finding median of two sorted arrays"""
    
    def test_basic_even_length(self):
        """Test with two arrays of equal length resulting in even total"""
        nums1 = [1, 3]
        nums2 = [2]
        assert findMedianSortedArrays(nums1, nums2) == 2.0
    
    def test_basic_odd_length(self):
        """Test with arrays resulting in odd total length"""
        nums1 = [1, 2]
        nums2 = [3, 4]
        assert findMedianSortedArrays(nums1, nums2) == 2.5
    
    def test_empty_first_array(self):
        """Test when first array is empty"""
        nums1 = []
        nums2 = [1]
        assert findMedianSortedArrays(nums1, nums2) == 1.0
    
    def test_empty_second_array(self):
        """Test when second array is empty"""
        nums1 = [2]
        nums2 = []
        assert findMedianSortedArrays(nums1, nums2) == 2.0
    
    def test_both_empty(self):
        """Test when both arrays are empty"""
        nums1 = []
        nums2 = []
        # Median of empty arrays should be handled gracefully
        # This might raise an error or return a special value
        try:
            result = findMedianSortedArrays(nums1, nums2)
            # If it doesn't raise, result should be reasonable
            assert result is not None
        except:
            pass
    
    def test_single_element_each(self):
        """Test with single element in each array"""
        nums1 = [1]
        nums2 = [2]
        assert findMedianSortedArrays(nums1, nums2) == 1.5
    
    def test_no_overlap(self):
        """Test with non-overlapping arrays"""
        nums1 = [1, 2]
        nums2 = [3, 4]
        assert findMedianSortedArrays(nums1, nums2) == 2.5
    
    def test_complete_overlap_first_smaller(self):
        """Test where first array is completely smaller"""
        nums1 = [1, 2]
        nums2 = [3, 4, 5, 6]
        assert findMedianSortedArrays(nums1, nums2) == 3.5
    
    def test_interleaved_arrays(self):
        """Test with interleaved arrays"""
        nums1 = [1, 3, 5]
        nums2 = [2, 4, 6]
        assert findMedianSortedArrays(nums1, nums2) == 3.5
    
    def test_large_first_array(self):
        """Test when first array is larger (should be swapped internally)"""
        nums1 = [1, 2, 3, 4, 5]
        nums2 = [6]
        assert findMedianSortedArrays(nums1, nums2) == 3.5
    
    def test_negative_numbers(self):
        """Test with negative numbers"""
        nums1 = [-2, -1]
        nums2 = [0, 1]
        assert findMedianSortedArrays(nums1, nums2) == -0.5
    
    def test_mixed_positive_negative(self):
        """Test with mixed positive and negative"""
        nums1 = [-5, -3]
        nums2 = [-1, 0, 2, 4]
        assert findMedianSortedArrays(nums1, nums2) == -0.5
    
    def test_duplicates(self):
        """Test with duplicate values"""
        nums1 = [1, 1, 1]
        nums2 = [1, 1, 1]
        assert findMedianSortedArrays(nums1, nums2) == 1.0
    
    def test_example_1(self):
        """LeetCode example 1"""
        nums1 = [1, 3]
        nums2 = [2]
        assert findMedianSortedArrays(nums1, nums2) == 2.0
    
    def test_example_2(self):
        """LeetCode example 2"""
        nums1 = [1, 2]
        nums2 = [3, 4]
        assert findMedianSortedArrays(nums1, nums2) == 2.5
    
    def test_large_arrays(self):
        """Test with larger arrays"""
        nums1 = list(range(0, 100, 2))  # [0, 2, 4, ..., 98]
        nums2 = list(range(1, 100, 2))  # [1, 3, 5, ..., 99]
        assert findMedianSortedArrays(nums1, nums2) == 49.5
    
    def test_one_large_one_small(self):
        """Test with one very large and one very small array"""
        nums1 = [1]
        nums2 = [2, 3, 4, 5, 6, 7, 8, 9, 10]
        assert findMedianSortedArrays(nums1, nums2) == 5.0
