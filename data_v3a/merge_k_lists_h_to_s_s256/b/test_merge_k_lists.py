import pytest
from merge_k_lists import ListNode, mergeKLists


def build_list(values):
    """Helper to build a linked list from a list of values."""
    if not values:
        return None
    head = ListNode(values[0])
    current = head
    for val in values[1:]:
        current.next = ListNode(val)
        current = current.next
    return head


def list_to_array(node):
    """Helper to convert a linked list to a Python list."""
    result = []
    while node:
        result.append(node.val)
        node = node.next
    return result


# --- Basic Tests ---

def test_basic_three_lists():
    """Merge 3 small sorted lists."""
    lists = [
        build_list([1, 4, 5]),
        build_list([1, 3, 4]),
        build_list([2, 6]),
    ]
    result = mergeKLists(lists)
    assert list_to_array(result) == [1, 1, 2, 3, 4, 4, 5, 6]


def test_empty_input():
    """Empty input list returns None."""
    result = mergeKLists([])
    assert result is None


def test_lists_with_none_values():
    """Input list containing None entries."""
    result = mergeKLists([None, None])
    assert result is None


def test_single_list():
    """Single list is returned as-is (sorted)."""
    lists = [build_list([1, 2, 3])]
    result = mergeKLists(lists)
    assert list_to_array(result) == [1, 2, 3]


def test_single_empty_list():
    """Single list that is None."""
    result = mergeKLists([None])
    assert result is None


def test_varying_lengths():
    """Lists of different lengths."""
    lists = [
        build_list([1, 10, 100]),
        build_list([2]),
        build_list([3, 4, 5, 6, 7]),
    ]
    result = mergeKLists(lists)
    assert list_to_array(result) == [1, 2, 3, 4, 5, 6, 7, 10, 100]


def test_duplicate_values_across_lists():
    """Duplicate values across multiple lists."""
    lists = [
        build_list([1, 1, 1]),
        build_list([1, 1]),
        build_list([1]),
    ]
    result = mergeKLists(lists)
    assert list_to_array(result) == [1, 1, 1, 1, 1, 1]


def test_two_lists():
    """Merge two sorted lists."""
    lists = [
        build_list([1, 3, 5]),
        build_list([2, 4, 6]),
    ]
    result = mergeKLists(lists)
    assert list_to_array(result) == [1, 2, 3, 4, 5, 6]


def test_single_element_lists():
    """Each list has exactly one element."""
    lists = [
        build_list([5]),
        build_list([3]),
        build_list([1]),
        build_list([4]),
        build_list([2]),
    ]
    result = mergeKLists(lists)
    assert list_to_array(result) == [1, 2, 3, 4, 5]


def test_mixed_none_and_valid_lists():
    """Mix of None and valid lists."""
    lists = [
        None,
        build_list([1, 3]),
        None,
        build_list([2, 4]),
    ]
    result = mergeKLists(lists)
    assert list_to_array(result) == [1, 2, 3, 4]


def test_negative_values():
    """Lists containing negative numbers."""
    lists = [
        build_list([-3, -1, 2]),
        build_list([-2, 0, 3]),
    ]
    result = mergeKLists(lists)
    assert list_to_array(result) == [-3, -2, -1, 0, 2, 3]


def test_large_k():
    """Many lists each with one element."""
    lists = [build_list([i]) for i in range(10, 0, -1)]
    result = mergeKLists(lists)
    assert list_to_array(result) == list(range(1, 11))


def test_already_sorted_single_merged():
    """All elements already in order across lists."""
    lists = [
        build_list([1, 2]),
        build_list([3, 4]),
        build_list([5, 6]),
    ]
    result = mergeKLists(lists)
    assert list_to_array(result) == [1, 2, 3, 4, 5, 6]
