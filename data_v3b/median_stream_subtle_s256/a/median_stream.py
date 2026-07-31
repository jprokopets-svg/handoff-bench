import heapq

class MedianFinder:
    """
    Maintains the median of a stream of numbers.
    - add_num(num): Add a number to the stream in O(log n) time
    - find_median(): Return the median in O(1) time
    """
    
    def __init__(self):
        # Max heap for the smaller half (use negative values since Python has min heap)
        self.small = []
        # Min heap for the larger half
        self.large = []
    
    def add_num(self, num: int) -> None:
        """
        Add a number to the stream.
        Time complexity: O(log n)
        """
        # Add to max heap (small) first
        heapq.heappush(self.small, -num)
        
        # Ensure every number in small is <= every number in large
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        
        # Maintain size property: small can have at most 1 more element than large
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        
        if len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)
    
    def find_median(self) -> float:
        """
        Return the median of the stream.
        Time complexity: O(1)
        """
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2.0
