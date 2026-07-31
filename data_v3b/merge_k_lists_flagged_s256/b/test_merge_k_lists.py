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
    """Helper function to convert a linked list to a list"""
    result = []
    current = head
    while current:
        result.append(current.val)
        current = current.next
    return result

def test_merge_k_lists_basic():
    """Test merging 3 sorted lists"""
    list1 = create_linked_list([1, 4, 5])
    list2 = create_linked_list([1, 3, 4])
    list3 = create_linked_list([2, 6])
    
    result = mergeKLists([list1, list2, list3])
    assert linked_list_to_list(result) == [1, 1, 2, 3, 4, 4, 5, 6]

def test_merge_k_lists_empty():
    """Test with empty list of lists"""
    result = mergeKLists([])
    assert result is None

def test_merge_k_lists_single_empty():
    """Test with a single empty list"""
    result = mergeKLists([None])
    assert result is None

def test_merge_k_lists_single_list():
    """Test with a single non-empty list"""
    list1 = create_linked_list([1, 2, 3])
    result = mergeKLists([list1])
    assert linked_list_to_list(result) == [1, 2, 3]

def test_merge_k_lists_multiple_empty():
    """Test with multiple empty lists"""
    result = mergeKLists([None, None, None])
    assert result is None

def test_merge_k_lists_mixed_empty():
    """Test with some empty and some non-empty lists"""
    list1 = create_linked_list([1, 4, 5])
    list2 = None
    list3 = create_linked_list([2, 6])
    
    result = mergeKLists([list1, list2, list3])
    assert linked_list_to_list(result) == [1, 2, 4, 5, 6]

def test_merge_k_lists_single_element():
    """Test with lists containing single elements"""
    list1 = create_linked_list([1])
    list2 = create_linked_list([2])
    list3 = create_linked_list([3])
    
    result = mergeKLists([list1, list2, list3])
    assert linked_list_to_list(result) == [1, 2, 3]
