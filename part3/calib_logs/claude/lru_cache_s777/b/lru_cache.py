class Node:
    """Node in the doubly linked list for LRU cache."""
    def __init__(self, key: int = 0, value: int = 0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    """
    LRU (Least Recently Used) Cache implementation with O(1) get and put operations.
    
    Uses a combination of:
    - Hash map (dict) for O(1) key lookup
    - Doubly linked list for O(1) node removal/insertion and LRU tracking
    
    Most recently used items are at the end of the list.
    Least recently used items are at the beginning (after dummy head).
    """
    
    def __init__(self, capacity: int):
        """
        Initialize the LRU cache.
        
        Args:
            capacity: Maximum number of items the cache can hold
        """
        self.capacity = capacity
        self.cache = {}  # key -> Node mapping
        
        # Dummy head and tail nodes to simplify edge cases
        self.head = Node()  # dummy head
        self.tail = Node()  # dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def get(self, key: int) -> int:
        """
        Get the value of a key if it exists in the cache.
        
        Args:
            key: The key to look up
            
        Returns:
            The value associated with the key, or -1 if not found.
            Accessing a key marks it as recently used.
        """
        if key not in self.cache:
            return -1
        
        node = self.cache[key]
        self._move_to_end(node)  # Mark as recently used
        return node.value
    
    def put(self, key: int, value: int) -> None:
        """
        Insert or update a key-value pair in the cache.
        
        If the key already exists, update its value and mark it as recently used.
        If the cache is at capacity, evict the least recently used item.
        
        Args:
            key: The key to insert or update
            value: The value to associate with the key
        """
        if key in self.cache:
            # Update existing key
            node = self.cache[key]
            node.value = value
            self._move_to_end(node)  # Mark as recently used
        else:
            # Add new key
            if len(self.cache) >= self.capacity:
                # Evict least recently used (first node after dummy head)
                self._remove_node(self.head.next)
            
            # Create and add new node
            node = Node(key, value)
            self.cache[key] = node
            self._add_to_end(node)
    
    def _move_to_end(self, node: Node) -> None:
        """Move a node to the end of the linked list (mark as most recently used)."""
        self._remove_node(node)
        self._add_to_end(node)
    
    def _remove_node(self, node: Node) -> None:
        """Remove a node from the linked list."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node
        del self.cache[node.key]
    
    def _add_to_end(self, node: Node) -> None:
        """Add a node to the end of the linked list (before dummy tail)."""
        prev_node = self.tail.prev
        prev_node.next = node
        node.prev = prev_node
        node.next = self.tail
        self.tail.prev = node
