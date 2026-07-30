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
    def test_empty_input(self):
        """Test with empty list of lists."""
        result = mergeKLists([])
        assert result is None

    def test_single_empty_list(self):
        """Test with a single None list."""
        result = mergeKLists([None])
        assert result is None

    def test_multiple_empty_lists(self):
        """Test with multiple None lists."""
        result = mergeKLists([None, None, None])
        assert result is None

    def test_single_list_single_node(self):
        """Test with a single list containing one node."""
        list1 = create_linked_list([1])
        result = mergeKLists([list1])
        assert linked_list_to_list(result) == [1]

    def test_single_list_multiple_nodes(self):
        """Test with a single list containing multiple nodes."""
        list1 = create_linked_list([1, 2, 3])
        result = mergeKLists([list1])
        assert linked_list_to_list(result) == [1, 2, 3]

    def test_two_sorted_lists(self):
        """Test merging two sorted lists."""
        list1 = create_linked_list([1, 4, 5])
        list2 = create_linked_list([1, 3, 4])
        result = mergeKLists([list1, list2])
        assert linked_list_to_list(result) == [1, 1, 3, 4, 4, 5]

    def test_three_sorted_lists(self):
        """Test merging three sorted lists."""
        list1 = create_linked_list([1, 4, 5])
        list2 = create_linked_list([1, 3, 4])
        list3 = create_linked_list([2, 6])
        result = mergeKLists([list1, list2, list3])
        assert linked_list_to_list(result) == [1, 1, 2, 3, 4, 4, 5, 6]

    def test_lists_with_different_lengths(self):
        """Test merging lists of varying lengths."""
        list1 = create_linked_list([1])
        list2 = create_linked_list([0, 2, 3, 4, 5])
        list3 = create_linked_list([1, 2])
        result = mergeKLists([list1, list2, list3])
        assert linked_list_to_list(result) == [0, 1, 1, 2, 2, 3, 4, 5]

    def test_lists_with_duplicates(self):
        """Test merging lists with duplicate values."""
        list1 = create_linked_list([1, 1, 1])
        list2 = create_linked_list([1, 1, 1])
        result = mergeKLists([list1, list2])
        assert linked_list_to_list(result) == [1, 1, 1, 1, 1, 1]

    def test_mixed_empty_and_nonempty_lists(self):
        """Test with a mix of empty and non-empty lists."""
        list1 = create_linked_list([1, 4, 5])
        list2 = None
        list3 = create_linked_list([1, 3, 4])
        result = mergeKLists([list1, list2, list3])
        assert linked_list_to_list(result) == [1, 1, 3, 4, 4, 5]

    def test_negative_numbers(self):
        """Test merging lists with negative numbers."""
        list1 = create_linked_list([-5, -3, 0])
        list2 = create_linked_list([-4, -1, 2])
        result = mergeKLists([list1, list2])
        assert linked_list_to_list(result) == [-5, -4, -3, -1, 0, 2]

    def test_large_k(self):
        """Test with many lists."""
        lists = [create_linked_list([i]) for i in range(10)]
        result = mergeKLists(lists)
        assert linked_list_to_list(result) == list(range(10))
