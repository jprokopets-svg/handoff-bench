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
    lists = [
        build_list([1, 4, 5]),
        build_list([1, 3, 4]),
        build_list([2, 6]),
    ]
    result = mergeKLists(lists)
    assert list_to_array(result) == [1, 1, 2, 3, 4, 4, 5, 6]


def test_two_lists():
    lists = [
        build_list([1, 3, 5]),
        build_list([2, 4, 6]),
    ]
    result = mergeKLists(lists)
    assert list_to_array(result) == [1, 2, 3, 4, 5, 6]


def test_single_list():
    lists = [build_list([1, 2, 3])]
    result = mergeKLists(lists)
    assert list_to_array(result) == [1, 2, 3]


# --- Edge Cases ---

def test_empty_input():
    result = mergeKLists([])
    assert result is None


def test_all_none_lists():
    result = mergeKLists([None, None, None])
    assert result is None


def test_single_none_list():
    result = mergeKLists([None])
    assert result is None


def test_mixed_none_and_valid():
    lists = [
        None,
        build_list([1, 3]),
        None,
        build_list([2, 4]),
    ]
    result = mergeKLists(lists)
    assert list_to_array(result) == [1, 2, 3, 4]


# --- Duplicate Values ---

def test_duplicate_values_across_lists():
    lists = [
        build_list([1, 1, 2]),
        build_list([1, 2, 2]),
    ]
    result = mergeKLists(lists)
    assert list_to_array(result) == [1, 1, 1, 2, 2, 2]


def test_all_same_values():
    lists = [
        build_list([5, 5]),
        build_list([5, 5]),
        build_list([5]),
    ]
    result = mergeKLists(lists)
    assert list_to_array(result) == [5, 5, 5, 5, 5]


# --- Single-Node Lists ---

def test_single_node_lists():
    lists = [
        build_list([3]),
        build_list([1]),
        build_list([2]),
    ]
    result = mergeKLists(lists)
    assert list_to_array(result) == [1, 2, 3]


def test_single_node_one_list():
    lists = [build_list([42])]
    result = mergeKLists(lists)
    assert list_to_array(result) == [42]


# --- Larger / Stress Cases ---

def test_already_sorted_lists():
    lists = [
        build_list([1, 2, 3]),
        build_list([4, 5, 6]),
        build_list([7, 8, 9]),
    ]
    result = mergeKLists(lists)
    assert list_to_array(result) == [1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_reverse_order_single_elements():
    lists = [build_list([i]) for i in range(10, 0, -1)]
    result = mergeKLists(lists)
    assert list_to_array(result) == list(range(1, 11))


def test_negative_values():
    lists = [
        build_list([-5, -3, -1]),
        build_list([-4, -2, 0]),
    ]
    result = mergeKLists(lists)
    assert list_to_array(result) == [-5, -4, -3, -2, -1, 0]


def test_mixed_negative_and_positive():
    lists = [
        build_list([-3, 0, 3]),
        build_list([-1, 1]),
    ]
    result = mergeKLists(lists)
    assert list_to_array(result) == [-3, -1, 0, 1, 3]


def test_result_is_listnodes():
    """Ensure the result is made of ListNode objects, not raw values."""
    lists = [build_list([1, 2]), build_list([3, 4])]
    result = mergeKLists(lists)
    assert isinstance(result, ListNode)
    assert isinstance(result.next, ListNode)
