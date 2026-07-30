"""
Test cases for merging k sorted linked lists.
"""

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


class TestMergeKLists:
    """Test suite for mergeKLists function."""
    
    def test_empty_list(self):
        """Test with empty list of lists."""
        result = mergeKLists([])
        assert result is None
    
    def test_single_list(self):
        """Test with a single sorted list."""
        list1 = create_linked_list([1, 2, 3])
        result = mergeKLists([list1])
        assert linked_list_to_list(result) == [1, 2, 3]
    
    def test_two_lists(self):
        """Test with two sorted lists."""
        list1 = create_linked_list([1, 3, 5])
        list2 = create_linked_list([2, 4, 6])
        result = mergeKLists([list1, list2])
        assert linked_list_to_list(result) == [1, 2, 3, 4, 5, 6]
    
    def test_three_lists(self):
        """Test with three sorted lists."""
        list1 = create_linked_list([1, 4, 7])
        list2 = create_linked_list([2, 5, 8])
        list3 = create_linked_list([3, 6, 9])
        result = mergeKLists([list1, list2, list3])
        assert linked_list_to_list(result) == [1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    def test_lists_with_none(self):
        """Test with None values in the list of lists."""
        list1 = create_linked_list([1, 3])
        list2 = None
        list3 = create_linked_list([2, 4])
        result = mergeKLists([list1, list2, list3])
        assert linked_list_to_list(result) == [1, 2, 3, 4]
    
    def test_all_none(self):
        """Test with all None values."""
        result = mergeKLists([None, None, None])
        assert result is None
    
    def test_different_lengths(self):
        """Test with lists of different lengths."""
        list1 = create_linked_list([1])
        list2 = create_linked_list([2, 3, 4, 5])
        list3 = create_linked_list([6, 7])
        result = mergeKLists([list1, list2, list3])
        assert linked_list_to_list(result) == [1, 2, 3, 4, 5, 6, 7]
    
    def test_duplicate_values(self):
        """Test with duplicate values across lists."""
        list1 = create_linked_list([1, 3, 3, 5])
        list2 = create_linked_list([2, 3, 4])
        result = mergeKLists([list1, list2])
        assert linked_list_to_list(result) == [1, 2, 3, 3, 3, 4, 5]
    
    def test_single_node_lists(self):
        """Test with single-node lists."""
        list1 = create_linked_list([5])
        list2 = create_linked_list([1])
        list3 = create_linked_list([3])
        result = mergeKLists([list1, list2, list3])
        assert linked_list_to_list(result) == [1, 3, 5]
    
    def test_negative_numbers(self):
        """Test with negative numbers."""
        list1 = create_linked_list([-5, -2, 0])
        list2 = create_linked_list([-3, 1, 4])
        result = mergeKLists([list1, list2])
        assert linked_list_to_list(result) == [-5, -3, -2, 0, 1, 4]
    
    def test_large_k(self):
        """Test with many lists."""
        lists = [create_linked_list([i]) for i in range(10)]
        result = mergeKLists(lists)
        assert linked_list_to_list(result) == list(range(10))
