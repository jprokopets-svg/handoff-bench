import pytest
from merge_k_lists import ListNode, mergeKLists


def create_linked_list(values):
    """Helper function to create a linked list from a list of values."""
    if not values:
        return None
    head = ListNode(values[0])
    current = head
    for val in values[1:]:
        current.next = ListNode(val)
        current = current.next
    return head


def linked_list_to_list(head):
    """Helper function to convert a linked list to a Python list."""
    result = []
    current = head
    while current:
        result.append(current.val)
        current = current.next
    return result


def test_merge_k_lists_basic():
    """Test merging 3 sorted lists."""
    list1 = create_linked_list([1, 4, 5])
    list2 = create_linked_list([1, 3, 4])
    list3 = create_linked_list([2, 6])
    
    result = mergeKLists([list1, list2, list3])
    assert linked_list_to_list(result) == [1, 1, 2, 3, 4, 4, 5, 6]


def test_merge_k_lists_empty():
    """Test with empty input."""
    result = mergeKLists([])
    assert result is None


def test_merge_k_lists_single_list():
    """Test with a single list."""
    list1 = create_linked_list([1, 2, 3])
    result = mergeKLists([list1])
    assert linked_list_to_list(result) == [1, 2, 3]


def test_merge_k_lists_with_none():
    """Test with None lists in the input."""
    list1 = create_linked_list([1, 4, 5])
    list2 = None
    list3 = create_linked_list([2, 6])
    
    result = mergeKLists([list1, list2, list3])
    assert linked_list_to_list(result) == [1, 2, 4, 5, 6]


def test_merge_k_lists_all_none():
    """Test with all None lists."""
    result = mergeKLists([None, None, None])
    assert result is None


def test_merge_k_lists_single_node():
    """Test with single-node lists."""
    list1 = create_linked_list([1])
    list2 = create_linked_list([2])
    list3 = create_linked_list([3])
    
    result = mergeKLists([list1, list2, list3])
    assert linked_list_to_list(result) == [1, 2, 3]


def test_merge_k_lists_different_lengths():
    """Test with lists of different lengths."""
    list1 = create_linked_list([1])
    list2 = create_linked_list([2, 3, 4, 5])
    list3 = create_linked_list([6, 7])
    
    result = mergeKLists([list1, list2, list3])
    assert linked_list_to_list(result) == [1, 2, 3, 4, 5, 6, 7]


def test_merge_k_lists_duplicates():
    """Test with duplicate values across lists."""
    list1 = create_linked_list([1, 1, 1])
    list2 = create_linked_list([1, 1, 1])
    list3 = create_linked_list([1, 1, 1])
    
    result = mergeKLists([list1, list2, list3])
    assert linked_list_to_list(result) == [1, 1, 1, 1, 1, 1, 1, 1, 1]


def test_merge_k_lists_two_lists():
    """Test with two lists."""
    list1 = create_linked_list([1, 3, 5])
    list2 = create_linked_list([2, 4, 6])
    
    result = mergeKLists([list1, list2])
    assert linked_list_to_list(result) == [1, 2, 3, 4, 5, 6]


def test_merge_k_lists_negative_numbers():
    """Test with negative numbers."""
    list1 = create_linked_list([-5, -2, 0])
    list2 = create_linked_list([-3, 1, 4])
    list3 = create_linked_list([-1, 2, 3])
    
    result = mergeKLists([list1, list2, list3])
    assert linked_list_to_list(result) == [-5, -3, -2, -1, 0, 1, 2, 3, 4]


def test_merge_k_lists_large_values():
    """Test with large values."""
    list1 = create_linked_list([100, 200, 300])
    list2 = create_linked_list([150, 250, 350])
    
    result = mergeKLists([list1, list2])
    assert linked_list_to_list(result) == [100, 150, 200, 250, 300, 350]
