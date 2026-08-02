class LRUCache:
    """A simple LRU (least-recently used) cache.

    get(key) -> value or -1 if not found. Accessing a key marks it as recently used.
    put(key, value) -> inserts or updates key. If insertion causes size to exceed
    capacity, evict the least-recently-used item.

    Both operations run in O(1) time on average using a hashmap + doubly-linked list.
    """

    class _Node:
        __slots__ = ("key", "value", "prev", "next")

        def __init__(self, key=None, value=None):
            self.key = key
            self.value = value
            self.prev = None
            self.next = None

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("capacity must be > 0")
        self.capacity = capacity
        self.cache = {}  # key -> Node
        # Dummy head and tail to avoid edge-case checks
        self.head = self._Node()
        self.tail = self._Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def _add_node(self, node):
        """Add node right after head (most recently used position)."""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node):
        """Remove node from the linked list."""
        prev = node.prev
        nxt = node.next
        if prev is not None:
            prev.next = nxt
        if nxt is not None:
            nxt.prev = prev
        node.prev = None
        node.next = None

    def _move_to_front(self, node):
        """Move an existing node to the front (most recently used)."""
        self._remove_node(node)
        self._add_node(node)

    def _pop_tail(self):
        """Pop the least recently used node (right before tail)."""
        node = self.tail.prev
        if node is self.head:
            return None
        self._remove_node(node)
        return node

    def get(self, key: int) -> int:
        node = self.cache.get(key)
        if not node:
            return -1
        # move to front and return value
        self._move_to_front(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        node = self.cache.get(key)
        if node:
            # update value and mark as recently used
            node.value = value
            self._move_to_front(node)
            return
        # insert new node
        new_node = self._Node(key, value)
        self.cache[key] = new_node
        self._add_node(new_node)
        self.size += 1
        if self.size > self.capacity:
            # evict LRU
            tail = self._pop_tail()
            if tail:
                # remove from cache dict
                try:
                    del self.cache[tail.key]
                except KeyError:
                    pass
                self.size -= 1
