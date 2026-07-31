import heapq

class MedianFinder:
    """
    Maintains the median of a stream of numbers.
    - add_num: O(log n)
    - find_median: O(1)

    Strategy: Use two heaps:
      - max_heap (left half): a max-heap storing the smaller half of numbers
      - min_heap (right half): a min-heap storing the larger half of numbers

    Invariants:
      - len(max_heap) == len(min_heap)  OR  len(max_heap) == len(min_heap) + 1
      - Every element in max_heap <= every element in min_heap
    """

    def __init__(self):
        # max-heap for the lower half (negate values for Python's min-heap)
        self._max_heap = []
        # min-heap for the upper half
        self._min_heap = []

    def add_num(self, num: float) -> None:
        """Add a number to the data structure. O(log n)."""
        # Push to max_heap first (negate for max-heap behaviour)
        heapq.heappush(self._max_heap, -num)

        # Balance: ensure max_heap top <= min_heap top
        if self._min_heap and (-self._max_heap[0]) > self._min_heap[0]:
            val = -heapq.heappop(self._max_heap)
            heapq.heappush(self._min_heap, val)

        # Balance sizes: max_heap may have at most 1 extra element
        if len(self._max_heap) > len(self._min_heap) + 1:
            val = -heapq.heappop(self._max_heap)
            heapq.heappush(self._min_heap, val)
        elif len(self._min_heap) > len(self._max_heap):
            val = heapq.heappop(self._min_heap)
            heapq.heappush(self._max_heap, -val)

    def find_median(self) -> float:
        """Return the current median. O(1)."""
        if not self._max_heap:
            raise ValueError("No numbers have been added yet.")

        if len(self._max_heap) > len(self._min_heap):
            # Odd total count: median is the top of max_heap
            return float(-self._max_heap[0])
        else:
            # Even total count: median is the average of both tops
            return (-self._max_heap[0] + self._min_heap[0]) / 2.0
