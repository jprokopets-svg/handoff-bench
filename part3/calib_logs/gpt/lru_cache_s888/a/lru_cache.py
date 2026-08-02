class Node:
    __slots__ = ('key', 'value', 'prev', 'next')
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.capacity = capacity
        self.cache = {}  # key -> node
        # dummy head and tail
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def _add_node(self, node: Node):
        # Always add right after head (most recently used)
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: Node):
        prev = node.prev
        nxt = node.next
        prev.next = nxt
        nxt.prev = prev
        node.prev = node.next = None

    def _move_to_front(self, node: Node):
        self._remove_node(node)
        self._add_node(node)

    def _pop_tail(self) -> Node:
        # remove least recently used (before tail)
        node = self.tail.prev
        if node is self.head:
            return None
        self._remove_node(node)
        return node

    def get(self, key: int) -> int:
        node = self.cache.get(key)
        if not node:
            return -1
        # move to front
        self._move_to_front(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        node = self.cache.get(key)
        if node:
            node.value = value
            self._move_to_front(node)
            return
        # new node
        new_node = Node(key, value)
        self.cache[key] = new_node
        self._add_node(new_node)
        self.size += 1
        if self.size > self.capacity:
            tail = self._pop_tail()
            if tail:
                del self.cache[tail.key]
                self.size -= 1
