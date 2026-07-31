import pytest
from median_two_sorted import findMedianSortedArrays


class TestMedianTwoSortedArrays:
    """Test cases for finding median of two sorted arrays."""
    
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
        """Test case: [1] and [] -> 1.0"""
        assert findMedianSortedArrays([1], []) == 1.0
    
    def test_both_empty(self):
        """Test case: [] and [] -> should handle gracefully"""
        # This is an edge case - behavior depends on requirements
        # Typically would return 0 or raise an error
        result = findMedianSortedArrays([], [])
        assert isinstance(result, float)
    
    def test_single_element_each(self):
        """Test case: [1] and [2] -> 1.5"""
        assert findMedianSortedArrays([1], [2]) == 1.5
    
    def test_single_element_each_reversed(self):
        """Test case: [2] and [1] -> 1.5"""
        assert findMedianSortedArrays([2], [1]) == 1.5
    
    def test_larger_arrays_even_length(self):
        """Test case: [1,3,5,7] and [2,4,6,8] -> 4.5"""
        assert findMedianSortedArrays([1, 3, 5, 7], [2, 4, 6, 8]) == 4.5
    
    def test_larger_arrays_odd_length(self):
        """Test case: [1,3,5] and [2,4,6] -> 3.5"""
        assert findMedianSortedArrays([1, 3, 5], [2, 4, 6]) == 3.5
    
    def test_no_overlap(self):
        """Test case: [1,2] and [3,4] -> 2.5"""
        assert findMedianSortedArrays([1, 2], [3, 4]) == 2.5
    
    def test_complete_overlap(self):
        """Test case: [1,2,3] and [1,2,3] -> 2.0"""
        assert findMedianSortedArrays([1, 2, 3], [1, 2, 3]) == 2.0
    
    def test_negative_numbers(self):
        """Test case: [-2, -1] and [0, 1] -> -0.5"""
        assert findMedianSortedArrays([-2, -1], [0, 1]) == -0.5
    
    def test_all_negative(self):
        """Test case: [-5, -3, -1] and [-4, -2] -> -3.0"""
        assert findMedianSortedArrays([-5, -3, -1], [-4, -2]) == -3.0
    
    def test_duplicates(self):
        """Test case: [1, 1, 1] and [1, 1, 1] -> 1.0"""
        assert findMedianSortedArrays([1, 1, 1], [1, 1, 1]) == 1.0
    
    def test_large_difference(self):
        """Test case: [1] and [1000000] -> 500000.5"""
        assert findMedianSortedArrays([1], [1000000]) == 500000.5
    
    def test_first_array_larger(self):
        """Test case: [1,2,3,4,5] and [1,2] -> 2.5"""
        # Should swap internally to make nums1 smaller
        assert findMedianSortedArrays([1, 2, 3, 4, 5], [1, 2]) == 2.5
    
    def test_second_array_much_larger(self):
        """Test case: [1] and [1,2,3,4,5,6,7,8,9] -> 5.0"""
        assert findMedianSortedArrays([1], [1, 2, 3, 4, 5, 6, 7, 8, 9]) == 5.0
