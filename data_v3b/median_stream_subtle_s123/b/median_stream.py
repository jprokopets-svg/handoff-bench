import heapq
from typing import Union


class MedianFinder:
    """
    A class that maintains the median of a stream of numbers.
    - add_num: O(log n) time complexity
    - find_median: O(1) time complexity
    
    Uses two heaps:
    - max_heap: stores the smaller half of numbers (as negative values for max heap behavior)
    - min_heap: stores the larger half of numbers
    """
    
    def __init__(self):
        """Initialize the MedianFinder with two heaps."""
        self.max_heap = []  # max heap for smaller half (using negative values)
        self.min_heap = []  # min heap for larger half
    
    def add_num(self, num: int) -> None:
        """
        Add a number to the stream and maintain heap invariants.
        Time complexity: O(log n)
        
        Args:
            num: The number to add to the stream
        """
        # Always add to max_heap first (smaller half)
        heapq.heappush(self.max_heap, -num)
        
        # Ensure every element in max_heap is <= every element in min_heap
        if self.max_heap and self.min_heap and (-self.max_heap[0] > self.min_heap[0]):
            max_val = -heapq.heappop(self.max_heap)
            min_val = heapq.heappop(self.min_heap)
            heapq.heappush(self.max_heap, -min_val)
            heapq.heappush(self.min_heap, max_val)
        
        # Balance the heaps: max_heap should have at most 1 more element than min_heap
        if len(self.max_heap) > len(self.min_heap) + 1:
            val = -heapq.heappop(self.max_heap)
            heapq.heappush(self.min_heap, val)
        
        if len(self.min_heap) > len(self.max_heap):
            val = heapq.heappop(self.min_heap)
            heapq.heappush(self.max_heap, -val)
    
    def find_median(self) -> Union[int, float]:
        """
        Find the median of the stream.
        Time complexity: O(1)
        
        Returns:
            The median value. If the total count is even, returns the average of two middle values.
            If odd, returns the middle value.
        """
        if len(self.max_heap) > len(self.min_heap):
            return float(-self.max_heap[0])
        
        return (-self.max_heap[0] + self.min_heap[0]) / 2.0
