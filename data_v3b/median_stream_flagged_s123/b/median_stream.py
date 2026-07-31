import heapq
from typing import Union


class MedianFinder:
    """
    Maintains the median of a stream of numbers.
    - add_num: O(log n) time complexity
    - find_median: O(1) time complexity
    """
    
    def __init__(self):
        """Initialize the MedianFinder with two heaps."""
        # Max heap for smaller half (use negative values since Python has min heap)
        self.small = []
        # Min heap for larger half
        self.large = []
    
    def add_num(self, num: int) -> None:
        """
        Add a number to the stream.
        
        Args:
            num: The number to add
        """
        # Add to max heap (small) by negating the value
        heapq.heappush(self.small, -num)
        
        # Ensure every number in small is <= every number in large
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        
        # Ensure sizes are balanced (small can have at most 1 more element)
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        
        if len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)
    
    def find_median(self) -> Union[int, float]:
        """
        Find the median of the stream.
        
        Returns:
            The median value. If even number of elements, returns average of two middle elements.
        """
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        
        return (-self.small[0] + self.large[0]) / 2.0
