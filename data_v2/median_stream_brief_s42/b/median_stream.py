import heapq


class MedianFinder:
    """
    A class that maintains the median of a stream of numbers.
    
    Uses two heaps:
    - max_heap: stores the smaller half of numbers (negated for max heap behavior)
    - min_heap: stores the larger half of numbers
    
    Time complexity:
    - add_num: O(log n)
    - find_median: O(1)
    """
    
    def __init__(self):
        """Initialize the MedianFinder with two empty heaps."""
        self.max_heap = []  # max heap (use negative values)
        self.min_heap = []  # min heap
    
    def add_num(self, num: int) -> None:
        """
        Add a number to the stream.
        
        Args:
            num: The number to add
            
        Time complexity: O(log n)
        """
        # Always add to max_heap first (negated for max heap)
        heapq.heappush(self.max_heap, -num)
        
        # Ensure every element in max_heap is <= every element in min_heap
        if self.max_heap and self.min_heap:
            if (-self.max_heap[0]) > self.min_heap[0]:
                max_val = -heapq.heappop(self.max_heap)
                min_val = heapq.heappop(self.min_heap)
                heapq.heappush(self.max_heap, -min_val)
                heapq.heappush(self.min_heap, max_val)
        
        # Maintain size property: max_heap size should be equal to min_heap size
        # or one more than min_heap size
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
            
        Time complexity: O(1)
        """
        if len(self.max_heap) > len(self.min_heap):
            return float(-self.max_heap[0])
        
        return (-self.max_heap[0] + self.min_heap[0]) / 2.0
