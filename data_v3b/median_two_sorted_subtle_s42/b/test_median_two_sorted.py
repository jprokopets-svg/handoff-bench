import pytest
from median_two_sorted import findMedianSortedArrays


class TestMedianTwoSortedArrays:
    """Test cases for finding median of two sorted arrays."""
    
    def test_example1(self):
        """Test case: nums1=[1,3], nums2=[2]"""
        nums1 = [1, 3]
        nums2 = [2]
        assert findMedianSortedArrays(nums1, nums2) == 2.0
    
    def test_example2(self):
        """Test case: nums1=[1,2], nums2=[3,4]"""
        nums1 = [1, 2]
        nums2 = [3, 4]
        assert findMedianSortedArrays(nums1, nums2) == 2.5
    
    def test_empty_first_array(self):
        """Test case: nums1=[], nums2=[1]"""
        nums1 = []
        nums2 = [1]
        assert findMedianSortedArrays(nums1, nums2) == 1.0
    
    def test_empty_second_array(self):
        """Test case: nums1=[1], nums2=[]"""
        nums1 = [1]
        nums2 = []
        assert findMedianSortedArrays(nums1, nums2) == 1.0
    
    def test_single_element_each(self):
        """Test case: nums1=[1], nums2=[2]"""
        nums1 = [1]
        nums2 = [2]
        assert findMedianSortedArrays(nums1, nums2) == 1.5
    
    def test_larger_arrays(self):
        """Test case: nums1=[1,3,8,9,15], nums2=[7,11,18,19,21,25]"""
        nums1 = [1, 3, 8, 9, 15]
        nums2 = [7, 11, 18, 19, 21, 25]
        assert findMedianSortedArrays(nums1, nums2) == 11.0
    
    def test_all_first_smaller(self):
        """Test case: nums1=[1,2], nums2=[3,4,5,6]"""
        nums1 = [1, 2]
        nums2 = [3, 4, 5, 6]
        assert findMedianSortedArrays(nums1, nums2) == 3.5
    
    def test_all_second_smaller(self):
        """Test case: nums1=[5,6,7,8], nums2=[1,2]"""
        nums1 = [5, 6, 7, 8]
        nums2 = [1, 2]
        assert findMedianSortedArrays(nums1, nums2) == 4.5
    
    def test_interleaved(self):
        """Test case: nums1=[1,3,5,7], nums2=[2,4,6,8]"""
        nums1 = [1, 3, 5, 7]
        nums2 = [2, 4, 6, 8]
        assert findMedianSortedArrays(nums1, nums2) == 4.5
    
    def test_duplicates(self):
        """Test case: nums1=[1,1,1], nums2=[1,1,1]"""
        nums1 = [1, 1, 1]
        nums2 = [1, 1, 1]
        assert findMedianSortedArrays(nums1, nums2) == 1.0
