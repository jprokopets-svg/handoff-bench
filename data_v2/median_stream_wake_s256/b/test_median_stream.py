import pytest
from median_stream import MedianFinder


class TestMedianFinder:
    """Test suite for MedianFinder class."""
    
    def test_single_element(self):
        """Test with a single element."""
        mf = MedianFinder()
        mf.add_num(1)
        assert mf.find_median() == 1.0
    
    def test_two_elements(self):
        """Test with two elements."""
        mf = MedianFinder()
        mf.add_num(1)
        mf.add_num(2)
        assert mf.find_median() == 1.5
    
    def test_three_elements(self):
        """Test with three elements."""
        mf = MedianFinder()
        mf.add_num(1)
        mf.add_num(2)
        mf.add_num(3)
        assert mf.find_median() == 2.0
    
    def test_odd_number_of_elements(self):
        """Test with odd number of elements."""
        mf = MedianFinder()
        mf.add_num(1)
        mf.add_num(2)
        mf.add_num(3)
        mf.add_num(4)
        mf.add_num(5)
        assert mf.find_median() == 3.0
    
    def test_even_number_of_elements(self):
        """Test with even number of elements."""
        mf = MedianFinder()
        mf.add_num(1)
        mf.add_num(2)
        mf.add_num(3)
        mf.add_num(4)
        assert mf.find_median() == 2.5
    
    def test_negative_numbers(self):
        """Test with negative numbers."""
        mf = MedianFinder()
        mf.add_num(-1)
        mf.add_num(-2)
        mf.add_num(-3)
        assert mf.find_median() == -2.0
    
    def test_mixed_positive_negative(self):
        """Test with mixed positive and negative numbers."""
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
    
    def test_unordered_insertion(self):
        """Test with unordered insertion."""
        mf = MedianFinder()
        mf.add_num(5)
        mf.add_num(1)
        mf.add_num(3)
        mf.add_num(2)
        mf.add_num(4)
        assert mf.find_median() == 3.0
    
    def test_large_numbers(self):
        """Test with large numbers."""
        mf = MedianFinder()
        mf.add_num(1000000)
        mf.add_num(2000000)
        mf.add_num(3000000)
        assert mf.find_median() == 2000000.0
    
    def test_alternating_high_low(self):
        """Test with alternating high and low values."""
        mf = MedianFinder()
        mf.add_num(1)
        assert mf.find_median() == 1.0
        mf.add_num(100)
        assert mf.find_median() == 50.5
        mf.add_num(2)
        assert mf.find_median() == 2.0
        mf.add_num(99)
        assert mf.find_median() == 50.5
    
    def test_sequential_numbers(self):
        """Test with sequential numbers."""
        mf = MedianFinder()
        for i in range(1, 11):
            mf.add_num(i)
        assert mf.find_median() == 5.5
    
    def test_zero(self):
        """Test with zero."""
        mf = MedianFinder()
        mf.add_num(0)
        assert mf.find_median() == 0.0
    
    def test_zero_with_others(self):
        """Test with zero and other numbers."""
        mf = MedianFinder()
        mf.add_num(-5)
        mf.add_num(0)
        mf.add_num(5)
        assert mf.find_median() == 0.0
