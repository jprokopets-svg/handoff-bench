import heapq


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __lt__(self, other):
        return self.val < other.val

    def __eq__(self, other):
        return self.val == other.val


def merge_k_lists(lists):
    """
    Merge k sorted linked lists into one sorted linked list.

    :param lists: List of ListNode heads (each head starts a sorted linked list)
    :return: Head of the merged sorted linked list
    """
    heap = []

    # Push the head of each non-empty list onto the heap
    for node in lists:
        if node is not None:
            heapq.heappush(heap, node)

    dummy = ListNode(0)
    current = dummy

    while heap:
        # Pop the smallest node
        smallest = heapq.heappop(heap)
        current.next = smallest
        current = current.next

        # If this node has a next, push it onto the heap
        if smallest.next is not None:
            heapq.heappush(heap, smallest.next)

    return dummy.next


def list_to_linked(lst):
    """Helper: convert a Python list to a linked list, returns head node."""
    if not lst:
        return None
    head = ListNode(lst[0])
    current = head
    for val in lst[1:]:
        current.next = ListNode(val)
        current = current.next
    return head


def linked_to_list(node):
    """Helper: convert a linked list to a Python list."""
    result = []
    while node:
        result.append(node.val)
        node = node.next
    return result
