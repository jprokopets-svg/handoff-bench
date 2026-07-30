import heapq

class MedianFinder:
    """
    A class that maintains the median of a stream of numbers.
    
    Uses two heaps:
    - max_heap: stores the smaller half of numbers (negated for max heap behavior)
    - min_heap: stores the larger half of numbers
    
    Time Complexity:
    - add_num: O(log n)
    - find_median: O(1)
    """
    
    def __init__(self):
        """Initialize the MedianFinder with two heaps."""
        self.max_heap = []  # For smaller half (use negative values for max heap)
        self.min_heap = []  # For larger half
    
    def add_num(self, num: int) -> None:
        """
        Add a number to the stream and maintain the median.
        
        Args:
            num: The number to add to the stream
        """
        # Always add to max_heap first
        heapq.heappush(self.max_heap, -num)
        
        # Ensure every element in max_heap is <= every element in min_heap
        if self.max_heap and self.min_heap and (-self.max_heap[0] > self.min_heap[0]):
            max_val = -heapq.heappop(self.max_heap)
            min_val = heapq.heappop(self.min_heap)
            heapq.heappush(self.max_heap, -min_val)
            heapq.heappush(self.min_heap, max_val)
        
        # Balance the heaps - max_heap should have at most one more element
        if len(self.max_heap) > len(self.min_heap) + 1:
            val = -heapq.heappop(self.max_heap)
            heapq.heappush(self.min_heap, val)
        
        if len(self.min_heap) > len(self.max_heap):
            val = heapq.heappop(self.min_heap)
            heapq.heappush(self.max_heap, -val)
    
    def find_median(self) -> float:
        """
        Find the median of the stream.
        
        Returns:
            The median as a float
        """
        if len(self.max_heap) > len(self.min_heap):
            return float(-self.max_heap[0])
        else:
            return (-self.max_heap[0] + self.min_heap[0]) / 2.0
