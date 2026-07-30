import heapq
from typing import Union


class MedianFinder:
    """
    A class that maintains the median of a stream of numbers.
    - add_num: O(log n) time complexity
    - find_median: O(1) time complexity
    """
    
    def __init__(self):
        """Initialize the MedianFinder with two heaps."""
        # Max heap for the smaller half (use negative values for max heap in Python)
        self.small = []
        # Min heap for the larger half
        self.large = []
    
    def add_num(self, num: int) -> None:
        """
        Add a number to the stream.
        Time complexity: O(log n)
        """
        # Always add to small (max heap) first
        # Use negative value to simulate max heap
        heapq.heappush(self.small, -num)
        
        # Ensure every number in small is <= every number in large
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        
        # Maintain size property: small can have at most one more element than large
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        
        if len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)
    
    def find_median(self) -> Union[int, float]:
        """
        Find the median of the stream.
        Time complexity: O(1)
        """
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        
        # Both heaps have equal size
        return (-self.small[0] + self.large[0]) / 2.0
