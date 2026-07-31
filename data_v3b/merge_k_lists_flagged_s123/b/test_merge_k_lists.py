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
        """Test with empty input list."""
        result = mergeKLists([])
        assert result is None

    def test_single_empty_list(self):
        """Test with a single empty list."""
        result = mergeKLists([None])
        assert result is None

    def test_multiple_empty_lists(self):
        """Test with multiple empty lists."""
        result = mergeKLists([None, None, None])
        assert result is None

    def test_single_list_with_one_node(self):
        """Test with a single list containing one node."""
        list1 = create_linked_list([1])
        result = mergeKLists([list1])
        assert linked_list_to_list(result) == [1]

    def test_single_list_with_multiple_nodes(self):
        """Test with a single sorted list."""
        list1 = create_linked_list([1, 2, 3, 4, 5])
        result = mergeKLists([list1])
        assert linked_list_to_list(result) == [1, 2, 3, 4, 5]

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
        """Test merging lists of different lengths."""
        list1 = create_linked_list([1])
        list2 = create_linked_list([0])
        result = mergeKLists([list1, list2])
        assert linked_list_to_list(result) == [0, 1]

    def test_lists_with_duplicates(self):
        """Test merging lists with duplicate values."""
        list1 = create_linked_list([1, 1, 1])
        list2 = create_linked_list([1, 1, 1])
        result = mergeKLists([list1, list2])
        assert linked_list_to_list(result) == [1, 1, 1, 1, 1, 1]

    def test_many_lists(self):
        """Test merging many lists."""
        lists = [
            create_linked_list([1, 5, 9]),
            create_linked_list([2, 6, 10]),
            create_linked_list([3, 7, 11]),
            create_linked_list([4, 8, 12])
        ]
        result = mergeKLists(lists)
        assert linked_list_to_list(result) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    def test_lists_with_negative_numbers(self):
        """Test merging lists with negative numbers."""
        list1 = create_linked_list([-5, -2, 0])
        list2 = create_linked_list([-3, -1, 2])
        result = mergeKLists([list1, list2])
        assert linked_list_to_list(result) == [-5, -3, -2, -1, 0, 2]

    def test_mixed_empty_and_non_empty_lists(self):
        """Test with a mix of empty and non-empty lists."""
        list1 = create_linked_list([1, 3, 5])
        list2 = None
        list3 = create_linked_list([2, 4, 6])
        result = mergeKLists([list1, list2, list3])
        assert linked_list_to_list(result) == [1, 2, 3, 4, 5, 6]

    def test_large_values(self):
        """Test with large values."""
        list1 = create_linked_list([1000000, 2000000])
        list2 = create_linked_list([500000, 1500000])
        result = mergeKLists([list1, list2])
        assert linked_list_to_list(result) == [500000, 1000000, 1500000, 2000000]

    def test_result_is_sorted(self):
        """Verify the result is properly sorted."""
        list1 = create_linked_list([5, 10, 15])
        list2 = create_linked_list([1, 11, 20])
        list3 = create_linked_list([3, 8, 12])
        result = mergeKLists([list1, list2, list3])
        result_list = linked_list_to_list(result)
        assert result_list == sorted(result_list)
