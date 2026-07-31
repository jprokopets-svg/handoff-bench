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
    # Min heap to store (value, unique_id, node)
    # We need unique_id because ListNode objects aren't comparable
    min_heap = []
    
    # Add the first node from each list to the heap
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(min_heap, (lst.val, i, lst))
    
    # Create a dummy node to simplify the logic
    dummy = ListNode(0)
    current = dummy
    
    # Extract the minimum node and add the next node from that list
    while min_heap:
        val, idx, node = heapq.heappop(min_heap)
        current.next = node
        current = current.next
        
        # If there's a next node in this list, add it to the heap
        if node.next:
            heapq.heappush(min_heap, (node.next.val, idx, node.next))
    
    return dummy.next
