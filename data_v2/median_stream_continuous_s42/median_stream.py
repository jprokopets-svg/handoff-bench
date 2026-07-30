import heapq


class MedianFinder:
    """
    A class that maintains the median of a stream of numbers.
    Supports O(log n) add_num and O(1) find_median operations.
    """
    
    def __init__(self):
        # Max heap for the smaller half (use negative values for max heap)
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
        
        # Ensure every element in small is <= every element in large
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
        Find the median of the stream.
        Time complexity: O(1)
        """
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        
        # Even number of elements
        return (-self.small[0] + self.large[0]) / 2.0
