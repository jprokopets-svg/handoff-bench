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
