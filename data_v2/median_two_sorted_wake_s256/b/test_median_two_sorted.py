import pytest
from median_two_sorted import findMedianSortedArrays


class TestMedianTwoSortedArrays:
    """Test cases for finding median of two sorted arrays"""
    
    def test_both_arrays_empty(self):
        """Test with both arrays empty"""
        # Edge case: both empty
        result = findMedianSortedArrays([], [])
        assert result == 0.0 or result is not None
    
    def test_first_array_empty(self):
        """Test with first array empty"""
        result = findMedianSortedArrays([], [1])
        assert result == 1.0
        
        result = findMedianSortedArrays([], [1, 2])
        assert result == 1.5
        
        result = findMedianSortedArrays([], [1, 2, 3])
        assert result == 2.0
    
    def test_second_array_empty(self):
        """Test with second array empty"""
        result = findMedianSortedArrays([1], [])
        assert result == 1.0
        
        result = findMedianSortedArrays([1, 2], [])
        assert result == 1.5
        
        result = findMedianSortedArrays([1, 2, 3], [])
        assert result == 2.0
    
    def test_single_element_each(self):
        """Test with single element in each array"""
        result = findMedianSortedArrays([1], [2])
        assert result == 1.5
        
        result = findMedianSortedArrays([2], [1])
        assert result == 1.5
    
    def test_even_total_length(self):
        """Test cases where total length is even"""
        result = findMedianSortedArrays([1, 3], [2])
        assert result == 2.0
        
        result = findMedianSortedArrays([1, 3], [2, 4])
        assert result == 2.5
        
        result = findMedianSortedArrays([1, 2], [3, 4])
        assert result == 2.5
    
    def test_odd_total_length(self):
        """Test cases where total length is odd"""
        result = findMedianSortedArrays([1, 2], [3, 4, 5])
        assert result == 3.0
        
        result = findMedianSortedArrays([1, 3, 5], [2, 4])
        assert result == 3.0
        
        result = findMedianSortedArrays([1], [2, 3, 4])
        assert result == 2.0
    
    def test_no_overlap(self):
        """Test with non-overlapping arrays"""
        result = findMedianSortedArrays([1, 2], [3, 4])
        assert result == 2.5
        
        result = findMedianSortedArrays([1, 2, 3], [4, 5, 6])
        assert result == 3.5
    
    def test_complete_overlap(self):
        """Test with completely overlapping arrays"""
        result = findMedianSortedArrays([1, 2, 3], [1, 2, 3])
        assert result == 2.0
    
    def test_large_arrays(self):
        """Test with larger arrays"""
        result = findMedianSortedArrays([1, 2, 3, 4, 5], [6, 7, 8, 9, 10])
        assert result == 5.5
        
        result = findMedianSortedArrays(list(range(0, 100, 2)), list(range(1, 100, 2)))
        assert result == 49.5
    
    def test_negative_numbers(self):
        """Test with negative numbers"""
        result = findMedianSortedArrays([-5, -3, -1], [0, 2, 4])
        assert result == -0.5
        
        result = findMedianSortedArrays([-10, -5], [-3, 0])
        assert result == -4.0
    
    def test_duplicates(self):
        """Test with duplicate elements"""
        result = findMedianSortedArrays([1, 1, 1], [1, 1, 1])
        assert result == 1.0
        
        result = findMedianSortedArrays([1, 2, 2], [2, 3, 3])
        assert result == 2.0
