import pytest
from merge_k_lists import mergeKLists, ListNode


def create_linked_list(values):
    """Helper function to create a linked list from a list of values"""
    if not values:
        return None
    head = ListNode(values[0])
    current = head
    for val in values[1:]:
        current.next = ListNode(val)
        current = current.next
    return head


def linked_list_to_list(head):
    """Helper function to convert a linked list to a list of values"""
    result = []
    current = head
    while current:
        result.append(current.val)
        current = current.next
    return result


def test_merge_k_lists_basic():
    """Test merging 3 sorted lists"""
    lists = [
        create_linked_list([1, 4, 5]),
        create_linked_list([1, 3, 4]),
        create_linked_list([2, 6])
    ]
    result = mergeKLists(lists)
    assert linked_list_to_list(result) == [1, 1, 2, 3, 4, 4, 5, 6]


def test_merge_k_lists_empty():
    """Test with empty list"""
    result = mergeKLists([])
    assert result is None


def test_merge_k_lists_single_list():
    """Test with a single list"""
    lists = [create_linked_list([1, 2, 3])]
    result = mergeKLists(lists)
    assert linked_list_to_list(result) == [1, 2, 3]


def test_merge_k_lists_with_empty_lists():
    """Test with some empty lists"""
    lists = [
        create_linked_list([1, 4, 5]),
        None,
        create_linked_list([2, 6])
    ]
    result = mergeKLists(lists)
    assert linked_list_to_list(result) == [1, 2, 4, 5, 6]


def test_merge_k_lists_all_empty():
    """Test with all None lists"""
    lists = [None, None, None]
    result = mergeKLists(lists)
    assert result is None


def test_merge_k_lists_single_element():
    """Test with single element lists"""
    lists = [
        create_linked_list([1]),
        create_linked_list([2]),
        create_linked_list([3])
    ]
    result = mergeKLists(lists)
    assert linked_list_to_list(result) == [1, 2, 3]


def test_merge_k_lists_duplicates():
    """Test with duplicate values"""
    lists = [
        create_linked_list([1, 1, 1]),
        create_linked_list([1, 1, 1]),
        create_linked_list([1, 1, 1])
    ]
    result = mergeKLists(lists)
    assert linked_list_to_list(result) == [1, 1, 1, 1, 1, 1, 1, 1, 1]
