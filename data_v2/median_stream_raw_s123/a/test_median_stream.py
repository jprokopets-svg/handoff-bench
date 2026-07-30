import pytest
from median_stream import MedianFinder


class TestMedianFinder:
    def test_single_number(self):
        mf = MedianFinder()
        mf.add_num(1)
        assert mf.find_median() == 1.0
    
    def test_two_numbers(self):
        mf = MedianFinder()
        mf.add_num(1)
        mf.add_num(2)
        assert mf.find_median() == 1.5
    
    def test_three_numbers(self):
        mf = MedianFinder()
        mf.add_num(1)
        mf.add_num(2)
        mf.add_num(3)
        assert mf.find_median() == 2.0
    
    def test_odd_count(self):
        mf = MedianFinder()
        mf.add_num(1)
        assert mf.find_median() == 1.0
        mf.add_num(2)
        assert mf.find_median() == 1.5
        mf.add_num(3)
        assert mf.find_median() == 2.0
    
    def test_even_count(self):
        mf = MedianFinder()
        mf.add_num(1)
        mf.add_num(2)
        mf.add_num(3)
        mf.add_num(4)
        assert mf.find_median() == 2.5
    
    def test_unordered_stream(self):
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
        mf = MedianFinder()
        mf.add_num(-1)
        assert mf.find_median() == -1.0
        mf.add_num(-2)
        assert mf.find_median() == -1.5
        mf.add_num(0)
        assert mf.find_median() == -1.0
    
    def test_duplicates(self):
        mf = MedianFinder()
        mf.add_num(1)
        mf.add_num(1)
        mf.add_num(1)
        assert mf.find_median() == 1.0
    
    def test_large_stream(self):
        mf = MedianFinder()
        numbers = [12, 4, 5, 3, 8, 7]
        for num in numbers:
            mf.add_num(num)
        # Sorted: [3, 4, 5, 7, 8, 12]
        # Median of 6 numbers: (5 + 7) / 2 = 6.0
        assert mf.find_median() == 6.0
    
    def test_example_from_leetcode(self):
        mf = MedianFinder()
        mf.add_num(1)
        assert mf.find_median() == 1.0
        mf.add_num(2)
        assert mf.find_median() == 1.5
        mf.add_num(3)
        assert mf.find_median() == 2.0
