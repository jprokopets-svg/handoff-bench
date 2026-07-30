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
        The head of the merged sorted linked list
    """
    if not lists:
        return None
    
    # Min heap to efficiently get the smallest node
    # Store tuples of (value, unique_id, node)
    min_heap = []
    
    # Initialize heap with the first node from each list
    for i, head in enumerate(lists):
        if head:
            heapq.heappush(min_heap, (head.val, i, head))
    
    # Create a dummy node to simplify the merging process
    dummy = ListNode(0)
    current = dummy
    
    # Process nodes from the heap
    while min_heap:
        val, idx, node = heapq.heappop(min_heap)
        
        # Add the node to the result list
        current.next = node
        current = current.next
        
        # If the node has a next node, add it to the heap
        if node.next:
            heapq.heappush(min_heap, (node.next.val, idx, node.next))
    
    return dummy.next
