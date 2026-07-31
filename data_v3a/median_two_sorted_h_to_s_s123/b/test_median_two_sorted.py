import pytest
from median_two_sorted import findMedianSortedArrays


class TestFindMedianSortedArrays:

    # --- Basic cases ---
    def test_odd_total_interleaved(self):
        """[1,3] + [2] -> median is 2.0"""
        assert findMedianSortedArrays([1, 3], [2]) == 2.0

    def test_even_total_adjacent(self):
        """[1,2] + [3,4] -> median is 2.5"""
        assert findMedianSortedArrays([1, 2], [3, 4]) == 2.5

    def test_all_zeros(self):
        """[0,0] + [0] -> median is 0.0"""
        assert findMedianSortedArrays([0, 0], [0]) == 0.0

    # --- Empty array cases ---
    def test_first_empty(self):
        """[] + [1] -> median is 1.0"""
        assert findMedianSortedArrays([], [1]) == 1.0

    def test_second_empty(self):
        """[2] + [] -> median is 2.0"""
        assert findMedianSortedArrays([2], []) == 2.0

    def test_first_empty_two_elements(self):
        """[] + [1,2] -> median is 1.5"""
        assert findMedianSortedArrays([], [1, 2]) == 1.5

    def test_first_empty_three_elements(self):
        """[] + [1,2,3] -> median is 2.0"""
        assert findMedianSortedArrays([], [1, 2, 3]) == 2.0

    # --- Single element arrays ---
    def test_single_elements_equal(self):
        """[1] + [1] -> median is 1.0"""
        assert findMedianSortedArrays([1], [1]) == 1.0

    def test_single_elements_different(self):
        """[1] + [3] -> median is 2.0"""
        assert findMedianSortedArrays([1], [3]) == 2.0

    def test_single_vs_multi(self):
        """[2] + [1,3,4] -> median is 2.5"""
        assert findMedianSortedArrays([2], [1, 3, 4]) == 2.5

    # --- Larger arrays ---
    def test_larger_even(self):
        """[1,3,5,7] + [2,4,6,8] -> median is 4.5"""
        assert findMedianSortedArrays([1, 3, 5, 7], [2, 4, 6, 8]) == 4.5

    def test_larger_odd(self):
        """[1,2,3,4,5] + [6,7,8,9,10] -> median is 5.5"""
        assert findMedianSortedArrays([1, 2, 3, 4, 5], [6, 7, 8, 9, 10]) == 5.5

    def test_one_array_all_smaller(self):
        """[1,2] + [3,4,5,6] -> median is 3.5"""
        assert findMedianSortedArrays([1, 2], [3, 4, 5, 6]) == 3.5

    def test_one_array_all_larger(self):
        """[5,6] + [1,2,3,4] -> median is 3.5"""
        assert findMedianSortedArrays([5, 6], [1, 2, 3, 4]) == 3.5

    # --- Negative numbers ---
    def test_negative_numbers(self):
        """[-5,-3,-1] + [-4,-2,0] -> median is -2.5"""
        assert findMedianSortedArrays([-5, -3, -1], [-4, -2, 0]) == -2.5

    def test_mixed_negative_positive(self):
        """[-3,-1] + [1,3] -> median is 0.0"""
        assert findMedianSortedArrays([-3, -1], [1, 3]) == 0.0

    # --- Duplicate elements ---
    def test_duplicates_across_arrays(self):
        """[1,2,2] + [2,3,4] -> median is 2.0"""
        assert findMedianSortedArrays([1, 2, 2], [2, 3, 4]) == 2.0

    def test_all_same_elements(self):
        """[3,3,3] + [3,3,3] -> median is 3.0"""
        assert findMedianSortedArrays([3, 3, 3], [3, 3, 3]) == 3.0

    # --- Return type ---
    def test_returns_float(self):
        """Result should always be a float"""
        result = findMedianSortedArrays([1, 3], [2])
        assert isinstance(result, float)

    def test_even_returns_float(self):
        """Even total should return float"""
        result = findMedianSortedArrays([1, 2], [3, 4])
        assert isinstance(result, float)
