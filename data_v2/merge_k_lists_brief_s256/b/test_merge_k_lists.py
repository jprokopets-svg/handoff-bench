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
    def test_merge_three_lists(self):
        """Test merging three sorted lists."""
        list1 = create_linked_list([1, 4, 5])
        list2 = create_linked_list([1, 3, 4])
        list3 = create_linked_list([2, 6])
        
        result = mergeKLists([list1, list2, list3])
        assert linked_list_to_list(result) == [1, 1, 2, 3, 4, 4, 5, 6]
    
    def test_empty_input(self):
        """Test with empty input list."""
        result = mergeKLists([])
        assert result is None
    
    def test_lists_with_none(self):
        """Test with None values in the lists array."""
        list1 = create_linked_list([1, 2, 3])
        result = mergeKLists([None, list1, None])
        assert linked_list_to_list(result) == [1, 2, 3]
    
    def test_single_list(self):
        """Test with a single list."""
        list1 = create_linked_list([1, 2, 3])
        result = mergeKLists([list1])
        assert linked_list_to_list(result) == [1, 2, 3]
    
    def test_all_none(self):
        """Test with all None lists."""
        result = mergeKLists([None, None, None])
        assert result is None
    
    def test_single_node_lists(self):
        """Test with single-node lists."""
        list1 = create_linked_list([5])
        list2 = create_linked_list([2])
        list3 = create_linked_list([8])
        
        result = mergeKLists([list1, list2, list3])
        assert linked_list_to_list(result) == [2, 5, 8]
    
    def test_lists_different_lengths(self):
        """Test with lists of different lengths."""
        list1 = create_linked_list([1])
        list2 = create_linked_list([0])
        
        result = mergeKLists([list1, list2])
        assert linked_list_to_list(result) == [0, 1]
    
    def test_duplicate_values(self):
        """Test with duplicate values across lists."""
        list1 = create_linked_list([1, 1, 1])
        list2 = create_linked_list([1, 1, 1])
        
        result = mergeKLists([list1, list2])
        assert linked_list_to_list(result) == [1, 1, 1, 1, 1, 1]
    
    def test_negative_numbers(self):
        """Test with negative numbers."""
        list1 = create_linked_list([-5, -2, 0])
        list2 = create_linked_list([-3, 1, 4])
        
        result = mergeKLists([list1, list2])
        assert linked_list_to_list(result) == [-5, -3, -2, 0, 1, 4]
