import heapq
from typing import List, Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def mergeKLists(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    """
    Merge k sorted linked lists into one sorted list.
    
    Args:
        lists: A list of k sorted linked lists
        
    Returns:
        A single sorted linked list containing all elements
    """
    if not lists:
        return None
    
    # Use a min heap to efficiently get the smallest node
    # Store tuples of (value, unique_id, node) to handle comparison
    heap = []
    
    # Initialize heap with the first node from each list
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst.val, i, lst))
    
    # Create a dummy node to simplify the result building
    dummy = ListNode(0)
    current = dummy
    
    # Process all nodes
    while heap:
        val, idx, node = heapq.heappop(heap)
        
        # Add the smallest node to the result
        current.next = node
        current = current.next
        
        # If this node has a next node, add it to the heap
        if node.next:
            heapq.heappush(heap, (node.next.val, idx, node.next))
    
    return dummy.next
