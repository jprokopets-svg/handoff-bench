import heapq


class MedianFinder:
    """
    Maintains the median of a stream of numbers.

    Uses two heaps:
    - max_heap (lower half): a max-heap implemented as a min-heap with negated values
    - min_heap (upper half): a standard min-heap

    Invariants:
    - All elements in max_heap <= all elements in min_heap
    - len(max_heap) == len(min_heap)  OR  len(max_heap) == len(min_heap) + 1
      (max_heap holds the extra element when total count is odd)

    add_num: O(log n)
    find_median: O(1)
    """

    def __init__(self):
        self._max_heap = []  # lower half (negated for max-heap behaviour)
        self._min_heap = []  # upper half

    def add_num(self, num: float) -> None:
        """Add a number to the data structure."""
        # Push to max_heap first (negate for max-heap)
        heapq.heappush(self._max_heap, -num)

        # Balance: ensure max_heap top <= min_heap top
        if self._min_heap and (-self._max_heap[0]) > self._min_heap[0]:
            val = -heapq.heappop(self._max_heap)
            heapq.heappush(self._min_heap, val)

        # Rebalance sizes: max_heap may have at most 1 more element than min_heap
        if len(self._max_heap) > len(self._min_heap) + 1:
            val = -heapq.heappop(self._max_heap)
            heapq.heappush(self._min_heap, val)
        elif len(self._min_heap) > len(self._max_heap):
            val = heapq.heappop(self._min_heap)
            heapq.heappush(self._max_heap, -val)

    def find_median(self) -> float:
        """Return the median of all numbers added so far."""
        if not self._max_heap and not self._min_heap:
            raise ValueError("No numbers have been added yet.")

        if len(self._max_heap) > len(self._min_heap):
            # Odd total: median is the top of max_heap
            return float(-self._max_heap[0])
        else:
            # Even total: median is the average of both heap tops
            return (-self._max_heap[0] + self._min_heap[0]) / 2.0
