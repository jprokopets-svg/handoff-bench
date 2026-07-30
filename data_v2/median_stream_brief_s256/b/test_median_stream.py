import pytest
from median_stream import MedianFinder


class TestMedianFinder:
    """Test cases for MedianFinder class"""
    
    def test_single_number(self):
        """Test with a single number"""
        mf = MedianFinder()
        mf.add_num(1)
        assert mf.find_median() == 1.0
    
    def test_two_numbers(self):
        """Test with two numbers"""
        mf = MedianFinder()
        mf.add_num(1)
        mf.add_num(2)
        assert mf.find_median() == 1.5
    
    def test_three_numbers_odd(self):
        """Test with three numbers (odd count)"""
        mf = MedianFinder()
        mf.add_num(1)
        mf.add_num(2)
        mf.add_num(3)
        assert mf.find_median() == 2.0
    
    def test_four_numbers_even(self):
        """Test with four numbers (even count)"""
        mf = MedianFinder()
        mf.add_num(1)
        mf.add_num(2)
        mf.add_num(3)
        mf.add_num(4)
        assert mf.find_median() == 2.5
    
    def test_unordered_numbers(self):
        """Test with numbers added in random order"""
        mf = MedianFinder()
        mf.add_num(5)
        assert mf.find_median() == 5.0
        mf.add_num(15)
        assert mf.find_median() == 10.0
        mf.add_num(1)
        assert mf.find_median() == 5.0
        mf.add_num(3)
        assert mf.find_median() == 4.0
    
    def test_negative_numbers(self):
        """Test with negative numbers"""
        mf = MedianFinder()
        mf.add_num(-1)
        assert mf.find_median() == -1.0
        mf.add_num(-2)
        assert mf.find_median() == -1.5
        mf.add_num(0)
        assert mf.find_median() == -1.0
    
    def test_duplicate_numbers(self):
        """Test with duplicate numbers"""
        mf = MedianFinder()
        mf.add_num(1)
        mf.add_num(1)
        assert mf.find_median() == 1.0
        mf.add_num(1)
        assert mf.find_median() == 1.0
    
    def test_large_stream(self):
        """Test with a larger stream of numbers"""
        mf = MedianFinder()
        numbers = [12, 4, 5, 3, 8, 7]
        for num in numbers:
            mf.add_num(num)
        # Sorted: [3, 4, 5, 7, 8, 12]
        # Median of 6 numbers: (5 + 7) / 2 = 6.0
        assert mf.find_median() == 6.0
    
    def test_alternating_add_and_find(self):
        """Test alternating between add and find operations"""
        mf = MedianFinder()
        mf.add_num(1)
        assert mf.find_median() == 1.0
        mf.add_num(2)
        assert mf.find_median() == 1.5
        mf.add_num(3)
        assert mf.find_median() == 2.0
        mf.add_num(4)
        assert mf.find_median() == 2.5
        mf.add_num(5)
        assert mf.find_median() == 3.0
