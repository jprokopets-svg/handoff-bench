"""
Merge k sorted linked lists into one sorted list.
"""

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def mergeKLists(lists):
    """
    Merge k sorted linked lists into one sorted list.
    
    Args:
        lists: A list of ListNode objects representing k sorted linked lists
        
    Returns:
        A single ListNode representing the merged sorted linked list
    """
    if not lists:
        return None
    
    # Filter out None values
    lists = [lst for lst in lists if lst is not None]
    
    if not lists:
        return None
    
    # Use a min heap to efficiently get the smallest node
    import heapq
    
    # Create a min heap with (value, unique_id, node)
    # We need unique_id to break ties when values are equal
    heap = []
    node_id = 0
    
    # Add the first node from each list to the heap
    for lst in lists:
        if lst:
            heapq.heappush(heap, (lst.val, node_id, lst))
            node_id += 1
    
    # Create a dummy node to simplify the logic
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
