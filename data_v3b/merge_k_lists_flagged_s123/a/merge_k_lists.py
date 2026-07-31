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
        A single sorted linked list containing all nodes from input lists
    """
    if not lists:
        return None
    
    # Min heap to efficiently get the smallest node
    # Store tuples of (value, unique_id, node)
    min_heap = []
    
    # Add the first node from each list to the heap
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(min_heap, (lst.val, i, lst))
    
    # Create a dummy node to simplify the process
    dummy = ListNode(0)
    current = dummy
    
    # Process nodes from the heap
    while min_heap:
        val, idx, node = heapq.heappop(min_heap)
        
        # Add the current node to the result list
        current.next = node
        current = current.next
        
        # If the current node has a next node, add it to the heap
        if node.next:
            heapq.heappush(min_heap, (node.next.val, idx, node.next))
    
    return dummy.next
