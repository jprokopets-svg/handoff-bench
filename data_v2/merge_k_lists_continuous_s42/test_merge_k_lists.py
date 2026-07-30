from merge_k_lists import *


def ll(vals):
    if not vals: return None
    head = ListNode(vals[0])
    cur = head
    for v in vals[1:]:
        cur.next = ListNode(v)
        cur = cur.next
    return head

def to_list(n):
    r = []
    while n:
        r.append(n.val)
        n = n.next
    return r

def test_merge_k_lists_basic():
    assert to_list(merge_k_lists([ll([1,4,5]), ll([1,3,4]), ll([2,6])])) == [1,1,2,3,4,4,5,6]

def test_merge_k_lists_empty():
    assert merge_k_lists([]) is None

def test_merge_k_lists_single():
    assert to_list(merge_k_lists([ll([1])])) == [1]
