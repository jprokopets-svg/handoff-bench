from median_two_sorted import find_median_sorted_arrays

def test_example1():
    assert find_median_sorted_arrays([1,3], [2]) == 2.0

def test_example2():
    assert find_median_sorted_arrays([1,2], [3,4]) == 2.5

def test_example3():
    assert find_median_sorted_arrays([0,0], [0,0]) == 0.0

def test_example4():
    assert find_median_sorted_arrays([], [1]) == 1.0
