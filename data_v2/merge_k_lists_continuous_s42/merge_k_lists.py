import heapq

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def merge_k_lists(lists: list[ListNode | None]) -> ListNode | None:
    """
    Merge k sorted linked lists into one sorted list.
    
    Args:
        lists: A list of k sorted linked lists
        
    Returns:
        A single sorted linked list containing all elements
    """
    # Filter out None lists
    lists = [l for l in lists if l is not None]
    
    if not lists:
        return None
    
    # Use a min heap to efficiently get the smallest element
    # Store tuples of (value, unique_id, node) to handle ties
    heap = []
    
    # Initialize heap with the first node from each list
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))
    
    # Create a dummy node to simplify the merge process
    dummy = ListNode(0)
    current = dummy
    
    # Process all nodes
    while heap:
        val, idx, node = heapq.heappop(heap)
        
        # Add the current node to the result
        current.next = node
        current = current.next
        
        # If there's a next node in this list, add it to the heap
        if node.next:
            heapq.heappush(heap, (node.next.val, idx, node.next))
    
    return dummy.next
