import heapq


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __lt__(self, other):
        return self.val < other.val


def merge_k_lists(lists):
    """
    Merge k sorted linked lists into one sorted linked list.

    :param lists: List of ListNode (heads of sorted linked lists)
    :return: Head of the merged sorted linked list
    """
    heap = []

    # Push the head of each list into the min-heap
    for node in lists:
        if node is not None:
            heapq.heappush(heap, node)

    dummy = ListNode(0)
    current = dummy

    while heap:
        # Pop the smallest node
        node = heapq.heappop(heap)
        current.next = node
        current = current.next

        # Push the next node from the same list
        if node.next is not None:
            heapq.heappush(heap, node.next)

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
