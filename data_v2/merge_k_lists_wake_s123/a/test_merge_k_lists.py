"""
Test cases for merge k sorted linked lists
"""
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
    list1 = create_linked_list([1, 4, 5])
    list2 = create_linked_list([1, 3, 4])
    list3 = create_linked_list([2, 6])
    
    result = mergeKLists([list1, list2, list3])
    assert linked_list_to_list(result) == [1, 1, 2, 3, 4, 4, 5, 6]


def test_merge_k_lists_empty():
    """Test with empty list"""
    result = mergeKLists([])
    assert result is None


def test_merge_k_lists_single_list():
    """Test with a single list"""
    list1 = create_linked_list([1, 2, 3])
    result = mergeKLists([list1])
    assert linked_list_to_list(result) == [1, 2, 3]


def test_merge_k_lists_with_none():
    """Test with None values in the list"""
    list1 = create_linked_list([1, 4, 5])
    list2 = None
    list3 = create_linked_list([2, 6])
    
    result = mergeKLists([list1, list2, list3])
    assert linked_list_to_list(result) == [1, 2, 4, 5, 6]


def test_merge_k_lists_all_none():
    """Test with all None values"""
    result = mergeKLists([None, None, None])
    assert result is None


def test_merge_k_lists_single_element():
    """Test with single element lists"""
    list1 = create_linked_list([1])
    list2 = create_linked_list([2])
    list3 = create_linked_list([3])
    
    result = mergeKLists([list1, list2, list3])
    assert linked_list_to_list(result) == [1, 2, 3]


def test_merge_k_lists_duplicates():
    """Test with duplicate values"""
    list1 = create_linked_list([1, 1, 1])
    list2 = create_linked_list([1, 1, 1])
    
    result = mergeKLists([list1, list2])
    assert linked_list_to_list(result) == [1, 1, 1, 1, 1, 1]
