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
        lists: A list of sorted linked lists
        
    Returns:
        The head of the merged sorted linked list
    """
    # Use a min heap to efficiently get the smallest node
    min_heap = []
    
    # Initialize heap with the first node of each list
    for i, lst in enumerate(lists):
        if lst:
            # Store (value, unique_id, node) to handle comparison
            heapq.heappush(min_heap, (lst.val, i, lst))
    
    # Create a dummy node to simplify the logic
    dummy = ListNode(0)
    current = dummy
    
    # Process all nodes
    while min_heap:
        val, idx, node = heapq.heappop(min_heap)
        
        # Add the node with smallest value to result
        current.next = node
        current = current.next
        
        # If this node has a next node, add it to the heap
        if node.next:
            heapq.heappush(min_heap, (node.next.val, idx, node.next))
    
    return dummy.next
