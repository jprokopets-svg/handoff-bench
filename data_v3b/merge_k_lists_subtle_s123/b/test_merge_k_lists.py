import pytest
from merge_k_lists import ListNode, mergeKLists


def list_to_array(node):
    """Convert linked list to array for easy comparison"""
    result = []
    while node:
        result.append(node.val)
        node = node.next
    return result


def array_to_list(arr):
    """Convert array to linked list"""
    if not arr:
        return None
    head = ListNode(arr[0])
    current = head
    for val in arr[1:]:
        current.next = ListNode(val)
        current = current.next
    return head


class TestMergeKLists:
    def test_empty_lists(self):
        """Test with empty input"""
        result = mergeKLists([])
        assert result is None
    
    def test_single_empty_list(self):
        """Test with a single empty list"""
        result = mergeKLists([None])
        assert result is None
    
    def test_single_list_one_node(self):
        """Test with single list containing one node"""
        list1 = ListNode(1)
        result = mergeKLists([list1])
        assert list_to_array(result) == [1]
    
    def test_single_list_multiple_nodes(self):
        """Test with single sorted list"""
        list1 = array_to_list([1, 2, 3])
        result = mergeKLists([list1])
        assert list_to_array(result) == [1, 2, 3]
    
    def test_two_sorted_lists(self):
        """Test merging two sorted lists"""
        list1 = array_to_list([1, 3, 5])
        list2 = array_to_list([2, 4, 6])
        result = mergeKLists([list1, list2])
        assert list_to_array(result) == [1, 2, 3, 4, 5, 6]
    
    def test_three_sorted_lists(self):
        """Test merging three sorted lists"""
        list1 = array_to_list([1, 4, 7])
        list2 = array_to_list([2, 5, 8])
        list3 = array_to_list([3, 6, 9])
        result = mergeKLists([list1, list2, list3])
        assert list_to_array(result) == [1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    def test_lists_with_different_lengths(self):
        """Test merging lists of different lengths"""
        list1 = array_to_list([1, 5, 10])
        list2 = array_to_list([2, 3])
        list3 = array_to_list([4, 6, 7, 8, 9])
        result = mergeKLists([list1, list2, list3])
        assert list_to_array(result) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    def test_lists_with_duplicates(self):
        """Test merging lists with duplicate values"""
        list1 = array_to_list([1, 3, 3, 5])
        list2 = array_to_list([2, 3, 4])
        result = mergeKLists([list1, list2])
        assert list_to_array(result) == [1, 2, 3, 3, 3, 4, 5]
    
    def test_some_empty_lists(self):
        """Test with some empty lists mixed in"""
        list1 = array_to_list([1, 3, 5])
        list2 = None
        list3 = array_to_list([2, 4, 6])
        result = mergeKLists([list1, list2, list3])
        assert list_to_array(result) == [1, 2, 3, 4, 5, 6]
    
    def test_all_empty_lists(self):
        """Test with all None lists"""
        result = mergeKLists([None, None, None])
        assert result is None
    
    def test_single_node_lists(self):
        """Test merging multiple single-node lists"""
        list1 = ListNode(3)
        list2 = ListNode(1)
        list3 = ListNode(2)
        result = mergeKLists([list1, list2, list3])
        assert list_to_array(result) == [1, 2, 3]
