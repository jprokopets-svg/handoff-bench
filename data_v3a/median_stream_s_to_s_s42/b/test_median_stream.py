import pytest
from median_stream import MedianFinder


# ── Basic functionality ────────────────────────────────────────────────────────

def test_single_element():
    mf = MedianFinder()
    mf.add_num(5)
    assert mf.find_median() == 5.0


def test_two_elements():
    mf = MedianFinder()
    mf.add_num(1)
    mf.add_num(3)
    assert mf.find_median() == 2.0


def test_three_elements_odd_count():
    mf = MedianFinder()
    mf.add_num(1)
    mf.add_num(2)
    mf.add_num(3)
    assert mf.find_median() == 2.0


def test_four_elements_even_count():
    mf = MedianFinder()
    for n in [1, 2, 3, 4]:
        mf.add_num(n)
    assert mf.find_median() == 2.5


def test_median_after_each_insertion():
    mf = MedianFinder()
    mf.add_num(6)
    assert mf.find_median() == 6.0
    mf.add_num(10)
    assert mf.find_median() == 8.0
    mf.add_num(2)
    assert mf.find_median() == 6.0
    mf.add_num(6)
    assert mf.find_median() == 6.0
    mf.add_num(5)
    assert mf.find_median() == 6.0


# ── Edge cases ─────────────────────────────────────────────────────────────────

def test_duplicate_values():
    mf = MedianFinder()
    for _ in range(5):
        mf.add_num(7)
    assert mf.find_median() == 7.0


def test_negative_numbers():
    mf = MedianFinder()
    for n in [-5, -3, -1, -4, -2]:
        mf.add_num(n)
    assert mf.find_median() == -3.0


def test_mixed_positive_negative():
    mf = MedianFinder()
    for n in [-10, 10, -5, 5, 0]:
        mf.add_num(n)
    assert mf.find_median() == 0.0


def test_large_stream():
    mf = MedianFinder()
    numbers = list(range(1, 101))   # 1 … 100
    for n in numbers:
        mf.add_num(n)
    # Even count: median = (50 + 51) / 2 = 50.5
    assert mf.find_median() == 50.5


def test_reverse_insertion_order():
    mf = MedianFinder()
    for n in [5, 4, 3, 2, 1]:
        mf.add_num(n)
    assert mf.find_median() == 3.0


def test_float_inputs():
    mf = MedianFinder()
    mf.add_num(1.5)
    mf.add_num(2.5)
    assert mf.find_median() == 2.0


def test_empty_raises():
    mf = MedianFinder()
    with pytest.raises((ValueError, IndexError)):
        mf.find_median()


def test_return_type_is_float():
    mf = MedianFinder()
    mf.add_num(3)
    result = mf.find_median()
    assert isinstance(result, float)


# ── Stress / correctness against sorted reference ─────────────────────────────

def test_stress_random_order():
    import random
    random.seed(42)
    nums = random.sample(range(-500, 500), 99)   # odd count → exact middle
    mf = MedianFinder()
    for n in nums:
        mf.add_num(n)
    expected = float(sorted(nums)[len(nums) // 2])
    assert mf.find_median() == expected


def test_incremental_correctness():
    """Verify median is correct after every single insertion."""
    import random
    random.seed(0)
    nums = random.sample(range(1000), 50)
    mf = MedianFinder()
    seen = []
    for n in nums:
        mf.add_num(n)
        seen.append(n)
        s = sorted(seen)
        mid = len(s) // 2
        expected = float(s[mid]) if len(s) % 2 == 1 else (s[mid - 1] + s[mid]) / 2.0
        assert mf.find_median() == expected, (
            f"After inserting {seen}: expected {expected}, got {mf.find_median()}"
        )
