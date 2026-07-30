import pytest
from median_stream import MedianFinder


class TestMedianFinder:
    """Test cases for MedianFinder class."""
    
    def test_single_number(self):
        """Test with a single number."""
        mf = MedianFinder()
        mf.add_num(1)
        assert mf.find_median() == 1.0
    
    def test_two_numbers(self):
        """Test with two numbers."""
        mf = MedianFinder()
        mf.add_num(1)
        mf.add_num(2)
        assert mf.find_median() == 1.5
    
    def test_three_numbers_odd(self):
        """Test with three numbers (odd count)."""
        mf = MedianFinder()
        mf.add_num(1)
        mf.add_num(2)
        mf.add_num(3)
        assert mf.find_median() == 2.0
    
    def test_four_numbers_even(self):
        """Test with four numbers (even count)."""
        mf = MedianFinder()
        mf.add_num(1)
        mf.add_num(2)
        mf.add_num(3)
        mf.add_num(4)
        assert mf.find_median() == 2.5
    
    def test_unsorted_input(self):
        """Test with unsorted input."""
        mf = MedianFinder()
        mf.add_num(5)
        mf.add_num(15)
        mf.add_num(1)
        mf.add_num(3)
        # Sorted: [1, 3, 5, 15], median = (3 + 5) / 2 = 4.0
        assert mf.find_median() == 4.0
    
    def test_negative_numbers(self):
        """Test with negative numbers."""
        mf = MedianFinder()
        mf.add_num(-1)
        mf.add_num(0)
        mf.add_num(1)
        assert mf.find_median() == 0.0
    
    def test_duplicates(self):
        """Test with duplicate numbers."""
        mf = MedianFinder()
        mf.add_num(1)
        mf.add_num(1)
        mf.add_num(1)
        assert mf.find_median() == 1.0
    
    def test_large_sequence(self):
        """Test with a larger sequence."""
        mf = MedianFinder()
        nums = [12, 4, 5, 3, 8, 7]
        for num in nums:
            mf.add_num(num)
        # Sorted: [3, 4, 5, 7, 8, 12], median = (5 + 7) / 2 = 6.0
        assert mf.find_median() == 6.0
    
    def test_alternating_add_and_find(self):
        """Test alternating add and find operations."""
        mf = MedianFinder()
        mf.add_num(1)
        assert mf.find_median() == 1.0
        mf.add_num(2)
        assert mf.find_median() == 1.5
        mf.add_num(3)
        assert mf.find_median() == 2.0
    
    def test_all_same_numbers(self):
        """Test with all same numbers."""
        mf = MedianFinder()
        for _ in range(5):
            mf.add_num(42)
        assert mf.find_median() == 42.0
    
    def test_mixed_positive_negative(self):
        """Test with mixed positive and negative numbers."""
        mf = MedianFinder()
        mf.add_num(-5)
        mf.add_num(10)
        mf.add_num(-3)
        mf.add_num(7)
        # Sorted: [-5, -3, 7, 10], median = (-3 + 7) / 2 = 2.0
        assert mf.find_median() == 2.0
