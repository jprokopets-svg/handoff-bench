import pytest
from merge_k_lists import ListNode, mergeKLists


# ── helpers ──────────────────────────────────────────────────────────────────

def build_list(values):
    """Build a linked list from a Python list of values; return head."""
    if not values:
        return None
    head = ListNode(values[0])
    cur = head
    for v in values[1:]:
        cur.next = ListNode(v)
        cur = cur.next
    return head


def to_list(node):
    """Convert a linked list to a Python list of values."""
    result = []
    while node:
        result.append(node.val)
        node = node.next
    return result


# ── tests ─────────────────────────────────────────────────────────────────────

def test_empty_input():
    """No lists at all → None."""
    assert mergeKLists([]) is None


def test_single_empty_list():
    """A list containing one None entry → None."""
    assert mergeKLists([None]) is None


def test_multiple_empty_lists():
    """All lists are None → None."""
    assert mergeKLists([None, None, None]) is None


def test_single_list_single_node():
    """One list with one node → that node."""
    head = build_list([42])
    result = mergeKLists([head])
    assert to_list(result) == [42]


def test_single_list_multiple_nodes():
    """One list with multiple nodes → same list."""
    head = build_list([1, 3, 5])
    result = mergeKLists([head])
    assert to_list(result) == [1, 3, 5]


def test_two_lists_no_overlap():
    """Two lists whose ranges don't overlap."""
    l1 = build_list([1, 2, 3])
    l2 = build_list([4, 5, 6])
    result = mergeKLists([l1, l2])
    assert to_list(result) == [1, 2, 3, 4, 5, 6]


def test_two_lists_interleaved():
    """Two lists that interleave."""
    l1 = build_list([1, 3, 5])
    l2 = build_list([2, 4, 6])
    result = mergeKLists([l1, l2])
    assert to_list(result) == [1, 2, 3, 4, 5, 6]


def test_three_lists():
    """Classic three-list example."""
    l1 = build_list([1, 4, 5])
    l2 = build_list([1, 3, 4])
    l3 = build_list([2, 6])
    result = mergeKLists([l1, l2, l3])
    assert to_list(result) == [1, 1, 2, 3, 4, 4, 5, 6]


def test_lists_with_duplicates():
    """Duplicate values across lists are all preserved."""
    l1 = build_list([1, 1, 2])
    l2 = build_list([1, 2, 2])
    result = mergeKLists([l1, l2])
    assert to_list(result) == [1, 1, 1, 2, 2, 2]


def test_lists_of_unequal_length():
    """Lists of different lengths."""
    l1 = build_list([1])
    l2 = build_list([2, 3, 4, 5])
    l3 = build_list([0, 6])
    result = mergeKLists([l1, l2, l3])
    assert to_list(result) == [0, 1, 2, 3, 4, 5, 6]


def test_mixed_none_and_valid():
    """Some lists are None, others are valid."""
    l1 = build_list([1, 3])
    l2 = None
    l3 = build_list([2, 4])
    result = mergeKLists([l1, l2, l3])
    assert to_list(result) == [1, 2, 3, 4]


def test_negative_values():
    """Lists containing negative numbers."""
    l1 = build_list([-3, -1, 2])
    l2 = build_list([-2, 0, 3])
    result = mergeKLists([l1, l2])
    assert to_list(result) == [-3, -2, -1, 0, 2, 3]


def test_single_node_lists():
    """Each list has exactly one node."""
    lists = [build_list([v]) for v in [5, 1, 3, 2, 4]]
    result = mergeKLists(lists)
    assert to_list(result) == [1, 2, 3, 4, 5]


def test_result_is_sorted():
    """General property: output must always be non-decreasing."""
    import random
    random.seed(0)
    lists = []
    all_vals = []
    for _ in range(5):
        vals = sorted(random.randint(0, 100) for _ in range(random.randint(1, 10)))
        all_vals.extend(vals)
        lists.append(build_list(vals))
    result = to_list(mergeKLists(lists))
    assert result == sorted(all_vals)
