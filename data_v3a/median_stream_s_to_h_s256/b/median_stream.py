import heapq

class MedianFinder:
    """
    Maintains the median of a stream of numbers.
    
    Uses two heaps:
    - max_heap (left half): stores the smaller half of numbers (as negatives for max-heap behavior)
    - min_heap (right half): stores the larger half of numbers
    
    Invariants:
    - len(min_heap) <= len(max_heap) <= len(min_heap) + 1
    - Every element in max_heap <= every element in min_heap
    
    add_num: O(log n)
    find_median: O(1)
    """

    def __init__(self):
        self.max_heap = []  # left half (max-heap via negation)
        self.min_heap = []  # right half (min-heap)

    def add_num(self, num: float) -> None:
        """Add a number to the data structure."""
        # Push to max_heap first (negate for max-heap behavior)
        heapq.heappush(self.max_heap, -num)

        # Balance: ensure max_heap top <= min_heap top
        if self.min_heap and (-self.max_heap[0]) > self.min_heap[0]:
            val = -heapq.heappop(self.max_heap)
            heapq.heappush(self.min_heap, val)

        # Balance sizes: max_heap can have at most 1 more element than min_heap
        if len(self.max_heap) > len(self.min_heap) + 1:
            val = -heapq.heappop(self.max_heap)
            heapq.heappush(self.min_heap, val)
        elif len(self.min_heap) > len(self.max_heap):
            val = heapq.heappop(self.min_heap)
            heapq.heappush(self.max_heap, -val)

    def find_median(self) -> float:
        """Return the median of all numbers added so far."""
        if not self.max_heap and not self.min_heap:
            raise ValueError("No numbers have been added yet.")

        if len(self.max_heap) > len(self.min_heap):
            # Odd total count: median is the top of max_heap
            return float(-self.max_heap[0])
        else:
            # Even total count: median is average of both heap tops
            return (-self.max_heap[0] + self.min_heap[0]) / 2.0
