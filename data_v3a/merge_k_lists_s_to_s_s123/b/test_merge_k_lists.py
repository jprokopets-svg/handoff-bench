import pytest
from merge_k_lists import ListNode, merge_k_lists, list_to_linked, linked_to_list


def test_merge_three_sorted_lists():
    lists = [
        list_to_linked([1, 4, 5]),
        list_to_linked([1, 3, 4]),
        list_to_linked([2, 6]),
    ]
    result = merge_k_lists(lists)
    assert linked_to_list(result) == [1, 1, 2, 3, 4, 4, 5, 6]


def test_merge_empty_input():
    result = merge_k_lists([])
    assert result is None


def test_merge_single_empty_list():
    result = merge_k_lists([None])
    assert result is None


def test_merge_single_list():
    lists = [list_to_linked([1, 2, 3])]
    result = merge_k_lists(lists)
    assert linked_to_list(result) == [1, 2, 3]


def test_merge_two_lists():
    lists = [
        list_to_linked([1, 3, 5]),
        list_to_linked([2, 4, 6]),
    ]
    result = merge_k_lists(lists)
    assert linked_to_list(result) == [1, 2, 3, 4, 5, 6]


def test_merge_lists_with_duplicates():
    lists = [
        list_to_linked([1, 1, 1]),
        list_to_linked([1, 1]),
    ]
    result = merge_k_lists(lists)
    assert linked_to_list(result) == [1, 1, 1, 1, 1]


def test_merge_single_element_lists():
    lists = [
        list_to_linked([3]),
        list_to_linked([1]),
        list_to_linked([2]),
    ]
    result = merge_k_lists(lists)
    assert linked_to_list(result) == [1, 2, 3]


def test_merge_with_negative_values():
    lists = [
        list_to_linked([-3, -1, 2]),
        list_to_linked([-2, 0, 3]),
    ]
    result = merge_k_lists(lists)
    assert linked_to_list(result) == [-3, -2, -1, 0, 2, 3]


def test_merge_mixed_empty_and_nonempty():
    lists = [
        None,
        list_to_linked([1, 3]),
        None,
        list_to_linked([2, 4]),
    ]
    result = merge_k_lists(lists)
    assert linked_to_list(result) == [1, 2, 3, 4]
