import pytest
from median_stream import MedianFinder


# ── Basic single-element ──────────────────────────────────────────────────────

def test_single_element():
    mf = MedianFinder()
    mf.add_num(5)
    assert mf.find_median() == 5.0


# ── Two elements ──────────────────────────────────────────────────────────────

def test_two_elements():
    mf = MedianFinder()
    mf.add_num(1)
    mf.add_num(3)
    assert mf.find_median() == 2.0


# ── Three elements (odd count → exact middle) ─────────────────────────────────

def test_three_elements():
    mf = MedianFinder()
    for n in [1, 2, 3]:
        mf.add_num(n)
    assert mf.find_median() == 2.0


# ── Classic example from LeetCode 295 ────────────────────────────────────────

def test_leetcode_example():
    mf = MedianFinder()
    mf.add_num(1)
    mf.add_num(2)
    assert mf.find_median() == 1.5
    mf.add_num(3)
    assert mf.find_median() == 2.0


# ── Duplicate values ──────────────────────────────────────────────────────────

def test_duplicates():
    mf = MedianFinder()
    for n in [5, 5, 5, 5]:
        mf.add_num(n)
    assert mf.find_median() == 5.0


# ── Negative numbers ─────────────────────────────────────────────────────────

def test_negative_numbers():
    mf = MedianFinder()
    for n in [-3, -1, -2]:
        mf.add_num(n)
    assert mf.find_median() == -2.0


# ── Mixed positive and negative ───────────────────────────────────────────────

def test_mixed_sign():
    mf = MedianFinder()
    for n in [-5, 0, 5]:
        mf.add_num(n)
    assert mf.find_median() == 0.0


# ── Reverse-sorted input ──────────────────────────────────────────────────────

def test_reverse_sorted():
    mf = MedianFinder()
    for n in [9, 7, 5, 3, 1]:
        mf.add_num(n)
    assert mf.find_median() == 5.0


# ── Sorted input ──────────────────────────────────────────────────────────────

def test_sorted_input():
    mf = MedianFinder()
    for n in [1, 3, 5, 7, 9]:
        mf.add_num(n)
    assert mf.find_median() == 5.0


# ── Even count → average of two middle values ─────────────────────────────────

def test_even_count_average():
    mf = MedianFinder()
    for n in [1, 2, 3, 4]:
        mf.add_num(n)
    assert mf.find_median() == 2.5


# ── Floating-point inputs ─────────────────────────────────────────────────────

def test_float_inputs():
    mf = MedianFinder()
    mf.add_num(1.5)
    mf.add_num(2.5)
    assert mf.find_median() == pytest.approx(2.0)


# ── Large stream ──────────────────────────────────────────────────────────────

def test_large_stream():
    mf = MedianFinder()
    for n in range(1, 1001):   # 1 … 1000
        mf.add_num(n)
    # Even count: median = (500 + 501) / 2 = 500.5
    assert mf.find_median() == pytest.approx(500.5)


# ── Incremental medians are correct at every step ────────────────────────────

def test_incremental_medians():
    mf = MedianFinder()
    data = [6, 1, 3, 2, 4, 5]
    expected = [6.0, 3.5, 3.0, 2.5, 3.0, 3.5]
    for num, exp in zip(data, expected):
        mf.add_num(num)
        assert mf.find_median() == pytest.approx(exp), \
            f"After adding {num}: expected {exp}, got {mf.find_median()}"


# ── Empty finder raises ───────────────────────────────────────────────────────

def test_empty_raises():
    mf = MedianFinder()
    with pytest.raises((ValueError, IndexError)):
        mf.find_median()


# ── Multiple independent instances don't share state ─────────────────────────

def test_independent_instances():
    mf1 = MedianFinder()
    mf2 = MedianFinder()
    mf1.add_num(10)
    mf2.add_num(20)
    assert mf1.find_median() == 10.0
    assert mf2.find_median() == 20.0
