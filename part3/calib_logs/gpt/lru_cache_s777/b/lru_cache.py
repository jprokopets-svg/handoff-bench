class _Node:
    __slots__ = ("key", "value", "prev", "next")
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        if capacity < 0:
            raise ValueError("capacity must be non-negative")
        self.capacity = capacity
        self.cache = {}  # key -> node
        # Dummy head and tail nodes to avoid edge checks
        self.head = _Node()
        self.tail = _Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def _add_node(self, node: _Node) -> None:
        # Add right after head (most recently used)
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: _Node) -> None:
        prev = node.prev
        nxt = node.next
        if prev is not None:
            prev.next = nxt
        if nxt is not None:
            nxt.prev = prev
        node.prev = node.next = None

    def _move_to_head(self, node: _Node) -> None:
        self._remove_node(node)
        self._add_node(node)

    def _pop_tail(self) -> _Node:
        # Remove and return the least recently used node
        node = self.tail.prev
        if node is self.head:
            return None
        self._remove_node(node)
        return node

    def get(self, key: int) -> int:
        node = self.cache.get(key)
        if not node:
            return -1
        # move to head and return value
        self._move_to_head(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return
        node = self.cache.get(key)
        if node:
            # update and move to head
            node.value = value
            self._move_to_head(node)
        else:
            new_node = _Node(key, value)
            self.cache[key] = new_node
            self._add_node(new_node)
            self.size += 1
            if self.size > self.capacity:
                tail = self._pop_tail()
                if tail:
                    del self.cache[tail.key]
                    self.size -= 1
