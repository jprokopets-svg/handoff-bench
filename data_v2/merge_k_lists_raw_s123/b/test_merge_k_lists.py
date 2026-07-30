import pytest
from merge_k_lists import ListNode, mergeKLists


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
    """Helper function to convert a linked list to a list for easy comparison"""
    result = []
    current = head
    while current:
        result.append(current.val)
        current = current.next
    return result


def test_merge_k_lists_basic():
    """Test merging k sorted lists"""
    lists = [
        create_linked_list([1, 4, 5]),
        create_linked_list([1, 3, 4]),
        create_linked_list([2, 6])
    ]
    result = mergeKLists(lists)
    assert linked_list_to_list(result) == [1, 1, 2, 3, 4, 4, 5, 6]


def test_merge_k_lists_empty():
    """Test with empty list"""
    lists = []
    result = mergeKLists(lists)
    assert result is None


def test_merge_k_lists_single_empty():
    """Test with single empty list"""
    lists = [None]
    result = mergeKLists(lists)
    assert result is None


def test_merge_k_lists_single_list():
    """Test with single non-empty list"""
    lists = [create_linked_list([1, 2, 3])]
    result = mergeKLists(lists)
    assert linked_list_to_list(result) == [1, 2, 3]


def test_merge_k_lists_multiple_empty():
    """Test with multiple empty lists"""
    lists = [None, None, None]
    result = mergeKLists(lists)
    assert result is None


def test_merge_k_lists_mixed_empty():
    """Test with mix of empty and non-empty lists"""
    lists = [
        None,
        create_linked_list([1, 2]),
        None,
        create_linked_list([3, 4])
    ]
    result = mergeKLists(lists)
    assert linked_list_to_list(result) == [1, 2, 3, 4]


def test_merge_k_lists_single_elements():
    """Test with lists containing single elements"""
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


def test_merge_k_lists_large():
    """Test with larger lists"""
    lists = [
        create_linked_list([1, 5, 9]),
        create_linked_list([2, 6, 10]),
        create_linked_list([3, 7, 11]),
        create_linked_list([4, 8, 12])
    ]
    result = mergeKLists(lists)
    assert linked_list_to_list(result) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
