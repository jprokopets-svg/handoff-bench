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
    
    def test_three_elements_odd(self):
        """Test with three elements (odd count)."""
        mf = MedianFinder()
        mf.add_num(1)
        mf.add_num(2)
        mf.add_num(3)
        assert mf.find_median() == 2.0
    
    def test_four_elements_even(self):
        """Test with four elements (even count)."""
        mf = MedianFinder()
        mf.add_num(1)
        mf.add_num(2)
        mf.add_num(3)
        mf.add_num(4)
        assert mf.find_median() == 2.5
    
    def test_five_elements(self):
        """Test with five elements."""
        mf = MedianFinder()
        mf.add_num(1)
        mf.add_num(2)
        mf.add_num(3)
        mf.add_num(4)
        mf.add_num(5)
        assert mf.find_median() == 3.0
    
    def test_unordered_insertion(self):
        """Test with unordered insertion."""
        mf = MedianFinder()
        mf.add_num(3)
        mf.add_num(1)
        mf.add_num(2)
        assert mf.find_median() == 2.0
    
    def test_with_duplicates(self):
        """Test with duplicate numbers."""
        mf = MedianFinder()
        mf.add_num(1)
        mf.add_num(1)
        mf.add_num(1)
        assert mf.find_median() == 1.0
    
    def test_with_negative_numbers(self):
        """Test with negative numbers."""
        mf = MedianFinder()
        mf.add_num(-1)
        mf.add_num(0)
        mf.add_num(1)
        assert mf.find_median() == 0.0
    
    def test_with_mixed_negative_positive(self):
        """Test with mixed negative and positive numbers."""
        mf = MedianFinder()
        mf.add_num(-3)
        mf.add_num(-1)
        mf.add_num(2)
        mf.add_num(5)
        assert mf.find_median() == 0.5
    
    def test_large_sequence(self):
        """Test with a larger sequence."""
        mf = MedianFinder()
        nums = [5, 15, 1, 3, 8]
        for num in nums:
            mf.add_num(num)
        # Sorted: [1, 3, 5, 8, 15], median = 5
        assert mf.find_median() == 5.0
    
    def test_large_sequence_even(self):
        """Test with a larger even sequence."""
        mf = MedianFinder()
        nums = [5, 15, 1, 3, 8, 7]
        for num in nums:
            mf.add_num(num)
        # Sorted: [1, 3, 5, 7, 8, 15], median = (5 + 7) / 2 = 6.0
        assert mf.find_median() == 6.0
    
    def test_median_updates_correctly(self):
        """Test that median updates correctly as elements are added."""
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
    
    def test_reverse_order(self):
        """Test with reverse ordered insertion."""
        mf = MedianFinder()
        mf.add_num(5)
        mf.add_num(4)
        mf.add_num(3)
        mf.add_num(2)
        mf.add_num(1)
        assert mf.find_median() == 3.0
    
    def test_all_same_numbers(self):
        """Test with all same numbers."""
        mf = MedianFinder()
        for _ in range(5):
            mf.add_num(7)
        assert mf.find_median() == 7.0
    
    def test_two_different_values(self):
        """Test with only two different values."""
        mf = MedianFinder()
        mf.add_num(1)
        mf.add_num(2)
        mf.add_num(1)
        mf.add_num(2)
        assert mf.find_median() == 1.5
