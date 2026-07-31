import pytest
from merge_k_lists import ListNode, merge_k_lists


def list_to_linked(lst):
    """Convert a Python list to a linked list, return head."""
    if not lst:
        return None
    head = ListNode(lst[0])
    current = head
    for val in lst[1:]:
        current.next = ListNode(val)
        current = current.next
    return head


def linked_to_list(node):
    """Convert a linked list to a Python list."""
    result = []
    while node:
        result.append(node.val)
        node = node.next
    return result


def test_merge_three_lists():
    lists = [
        list_to_linked([1, 4, 5]),
        list_to_linked([1, 3, 4]),
        list_to_linked([2, 6]),
    ]
    result = merge_k_lists(lists)
    assert linked_to_list(result) == [1, 1, 2, 3, 4, 4, 5, 6]


def test_merge_empty_input():
    result = merge_k_lists([])
    assert result is None


def test_merge_single_empty_list():
    result = merge_k_lists([None])
    assert result is None


def test_merge_single_list():
    lists = [list_to_linked([1, 2, 3])]
    result = merge_k_lists(lists)
    assert linked_to_list(result) == [1, 2, 3]


def test_merge_two_lists():
    lists = [
        list_to_linked([1, 3, 5]),
        list_to_linked([2, 4, 6]),
    ]
    result = merge_k_lists(lists)
    assert linked_to_list(result) == [1, 2, 3, 4, 5, 6]


def test_merge_lists_with_duplicates():
    lists = [
        list_to_linked([1, 1, 1]),
        list_to_linked([1, 1, 1]),
    ]
    result = merge_k_lists(lists)
    assert linked_to_list(result) == [1, 1, 1, 1, 1, 1]


def test_merge_lists_with_negative_values():
    lists = [
        list_to_linked([-3, -1, 2]),
        list_to_linked([-2, 0, 3]),
    ]
    result = merge_k_lists(lists)
    assert linked_to_list(result) == [-3, -2, -1, 0, 2, 3]


def test_merge_single_element_lists():
    lists = [
        list_to_linked([5]),
        list_to_linked([1]),
        list_to_linked([3]),
    ]
    result = merge_k_lists(lists)
    assert linked_to_list(result) == [1, 3, 5]


def test_merge_with_some_empty_lists():
    lists = [
        list_to_linked([1, 3]),
        None,
        list_to_linked([2, 4]),
    ]
    result = merge_k_lists(lists)
    assert linked_to_list(result) == [1, 2, 3, 4]


def test_merge_all_empty_lists():
    lists = [None, None, None]
    result = merge_k_lists(lists)
    assert result is None
