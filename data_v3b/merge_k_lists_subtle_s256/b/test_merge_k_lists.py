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
    """Helper function to convert a linked list to a Python list"""
    result = []
    current = head
    while current:
        result.append(current.val)
        current = current.next
    return result


def test_empty_lists():
    """Test with empty input"""
    result = mergeKLists([])
    assert result is None


def test_single_empty_list():
    """Test with a single empty list"""
    result = mergeKLists([None])
    assert result is None


def test_single_list():
    """Test with a single list"""
    list1 = create_linked_list([1, 2, 3])
    result = mergeKLists([list1])
    assert linked_list_to_list(result) == [1, 2, 3]


def test_two_lists():
    """Test with two sorted lists"""
    list1 = create_linked_list([1, 3, 5])
    list2 = create_linked_list([2, 4, 6])
    result = mergeKLists([list1, list2])
    assert linked_list_to_list(result) == [1, 2, 3, 4, 5, 6]


def test_three_lists():
    """Test with three sorted lists"""
    list1 = create_linked_list([1, 4, 7])
    list2 = create_linked_list([2, 5, 8])
    list3 = create_linked_list([3, 6, 9])
    result = mergeKLists([list1, list2, list3])
    assert linked_list_to_list(result) == [1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_lists_with_duplicates():
    """Test with lists containing duplicate values"""
    list1 = create_linked_list([1, 3, 3])
    list2 = create_linked_list([1, 2, 3])
    result = mergeKLists([list1, list2])
    assert linked_list_to_list(result) == [1, 1, 2, 3, 3, 3]


def test_lists_different_lengths():
    """Test with lists of different lengths"""
    list1 = create_linked_list([1])
    list2 = create_linked_list([2, 3, 4, 5])
    list3 = create_linked_list([6, 7])
    result = mergeKLists([list1, list2, list3])
    assert linked_list_to_list(result) == [1, 2, 3, 4, 5, 6, 7]


def test_single_node_lists():
    """Test with single-node lists"""
    list1 = create_linked_list([5])
    list2 = create_linked_list([3])
    list3 = create_linked_list([7])
    result = mergeKLists([list1, list2, list3])
    assert linked_list_to_list(result) == [3, 5, 7]


def test_multiple_empty_lists():
    """Test with multiple empty lists"""
    result = mergeKLists([None, None, None])
    assert result is None


def test_mixed_empty_and_non_empty():
    """Test with mix of empty and non-empty lists"""
    list1 = create_linked_list([1, 3])
    list2 = None
    list3 = create_linked_list([2, 4])
    result = mergeKLists([list1, list2, list3])
    assert linked_list_to_list(result) == [1, 2, 3, 4]
