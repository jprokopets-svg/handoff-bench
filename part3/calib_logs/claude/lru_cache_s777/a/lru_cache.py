class LRUCache:
    """
    LRU (Least Recently Used) Cache implementation.
    - get(key): Returns the value if key exists, -1 otherwise. O(1) average time.
    - put(key, value): Inserts or updates a key-value pair. Evicts LRU item if capacity exceeded. O(1) average time.
    """
    
    def __init__(self, capacity: int):
        """Initialize the cache with a given capacity."""
        self.capacity = capacity
        # Dictionary to store key -> value mappings
        self.cache = {}
        # Dictionary to store key -> node mappings for the doubly linked list
        self.order = {}
        # Doubly linked list to track access order
        self.head = Node(0, 0)  # Dummy head
        self.tail = Node(0, 0)  # Dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def get(self, key: int) -> int:
        """Get the value of a key if it exists, otherwise return -1."""
        if key not in self.cache:
            return -1
        
        # Move the accessed node to the end (most recently used)
        node = self.order[key]
        self._move_to_end(node)
        
        return self.cache[key]
    
    def put(self, key: int, value: int) -> None:
        """Put a key-value pair in the cache. Evict LRU item if capacity exceeded."""
        if key in self.cache:
            # Update existing key
            self.cache[key] = value
            node = self.order[key]
            self._move_to_end(node)
        else:
            # Add new key
            if len(self.cache) >= self.capacity:
                # Evict the least recently used item (first item after head)
                lru_node = self.head.next
                self._remove_node(lru_node)
                del self.cache[lru_node.key]
                del self.order[lru_node.key]
            
            # Create new node and add to cache
            new_node = Node(key, value)
            self.cache[key] = value
            self.order[key] = new_node
            self._add_to_end(new_node)
    
    def _move_to_end(self, node: 'Node') -> None:
        """Move a node to the end of the doubly linked list (most recently used)."""
        self._remove_node(node)
        self._add_to_end(node)
    
    def _remove_node(self, node: 'Node') -> None:
        """Remove a node from the doubly linked list."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node
    
    def _add_to_end(self, node: 'Node') -> None:
        """Add a node to the end of the doubly linked list (before tail)."""
        prev_node = self.tail.prev
        prev_node.next = node
        node.prev = prev_node
        node.next = self.tail
        self.tail.prev = node


class Node:
    """Node for the doubly linked list."""
    def __init__(self, key: int, value: int):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None
