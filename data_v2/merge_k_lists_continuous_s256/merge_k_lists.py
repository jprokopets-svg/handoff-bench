import heapq
from typing import List, Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def merge_k_lists(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    """
    Merge k sorted linked lists into one sorted list.
    
    Args:
        lists: A list of k sorted linked lists
        
    Returns:
        A single sorted linked list containing all elements
    """
    if not lists:
        return None
    
    # Create a min heap with (value, unique_id, node)
    # We need unique_id to handle cases where values are equal
    heap = []
    node_id = 0
    
    # Add the first node of each list to the heap
    for lst in lists:
        if lst:
            heapq.heappush(heap, (lst.val, node_id, lst))
            node_id += 1
    
    # Create a dummy node to simplify the process
    dummy = ListNode(0)
    current = dummy
    
    # Process the heap
    while heap:
        val, _, node = heapq.heappop(heap)
        current.next = node
        current = current.next
        
        # If the current node has a next node, add it to the heap
        if node.next:
            heapq.heappush(heap, (node.next.val, node_id, node.next))
            node_id += 1
    
    return dummy.next
