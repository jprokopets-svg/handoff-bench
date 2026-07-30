import pytest
from merge_k_lists import ListNode, mergeKLists


def test_merge_k_lists_empty():
    """Test with empty list of lists"""
    result = mergeKLists([])
    assert result is None


def test_merge_k_lists_single_list():
    """Test with a single list"""
    head = ListNode(1, ListNode(2, ListNode(3)))
    result = mergeKLists([head])
    
    # Verify the result
    values = []
    current = result
    while current:
        values.append(current.val)
        current = current.next
    assert values == [1, 2, 3]


def test_merge_k_lists_multiple_lists():
    """Test with multiple sorted lists"""
    list1 = ListNode(1, ListNode(4, ListNode(5)))
    list2 = ListNode(1, ListNode(3, ListNode(4)))
    list3 = ListNode(2, ListNode(6))
    
    result = mergeKLists([list1, list2, list3])
    
    # Verify the result
    values = []
    current = result
    while current:
        values.append(current.val)
        current = current.next
    assert values == [1, 1, 2, 3, 4, 4, 5, 6]


def test_merge_k_lists_with_none():
    """Test with some None lists"""
    list1 = ListNode(1, ListNode(4, ListNode(5)))
    list2 = None
    list3 = ListNode(2, ListNode(6))
    
    result = mergeKLists([list1, list2, list3])
    
    # Verify the result
    values = []
    current = result
    while current:
        values.append(current.val)
        current = current.next
    assert values == [1, 2, 4, 5, 6]


def test_merge_k_lists_all_none():
    """Test with all None lists"""
    result = mergeKLists([None, None, None])
    assert result is None


def test_merge_k_lists_single_node_lists():
    """Test with single node lists"""
    list1 = ListNode(3)
    list2 = ListNode(1)
    list3 = ListNode(2)
    
    result = mergeKLists([list1, list2, list3])
    
    # Verify the result
    values = []
    current = result
    while current:
        values.append(current.val)
        current = current.next
    assert values == [1, 2, 3]


def test_merge_k_lists_duplicates():
    """Test with duplicate values"""
    list1 = ListNode(1, ListNode(1, ListNode(1)))
    list2 = ListNode(1, ListNode(1))
    
    result = mergeKLists([list1, list2])
    
    # Verify the result
    values = []
    current = result
    while current:
        values.append(current.val)
        current = current.next
    assert values == [1, 1, 1, 1, 1]
