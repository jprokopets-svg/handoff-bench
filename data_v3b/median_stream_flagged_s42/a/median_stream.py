import heapq


class MedianFinder:
    """
    A class that maintains the median of a stream of numbers.
    - add_num(num): Add a number to the stream in O(log n) time
    - find_median(): Return the median in O(1) time
    
    Uses two heaps:
    - small: max heap (negated values) for the smaller half of numbers
    - large: min heap for the larger half of numbers
    """
    
    def __init__(self):
        """Initialize the MedianFinder with two empty heaps."""
        self.small = []  # max heap (use negative values)
        self.large = []  # min heap
    
    def add_num(self, num: int) -> None:
        """
        Add a number to the stream.
        Time complexity: O(log n)
        """
        # Always add to small first (as negative for max heap behavior)
        heapq.heappush(self.small, -num)
        
        # Ensure every number in small <= every number in large
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        
        # Maintain size property: len(small) == len(large) or len(small) == len(large) + 1
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        
        if len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)
    
    def find_median(self) -> float:
        """
        Return the median of all numbers added so far.
        Time complexity: O(1)
        """
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        
        return (-self.small[0] + self.large[0]) / 2.0
