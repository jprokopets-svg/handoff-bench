class LRUCache:
    """
    LRU Cache implementation with O(1) average time for both get and put operations.
    Uses a combination of a dictionary (for O(1) lookups) and a doubly-linked list
    (for O(1) removal and insertion of elements).
    """
    
    class Node:
        """Node in the doubly-linked list"""
        def __init__(self, key=0, value=0):
            self.key = key
            self.value = value
            self.prev = None
            self.next = None
    
    def __init__(self, capacity: int):
        """
        Initialize the LRU cache with a given capacity.
        
        Args:
            capacity: Maximum number of items the cache can hold
        """
        self.capacity = capacity
        self.cache = {}  # Dictionary to store key -> Node mapping
        
        # Dummy head and tail nodes to simplify operations
        self.head = self.Node()  # Most recently used end
        self.tail = self.Node()  # Least recently used end
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _remove_node(self, node: Node) -> None:
        """Remove a node from the doubly-linked list"""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node
    
    def _add_to_head(self, node: Node) -> None:
        """Add a node right after the head (most recently used position)"""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
    
    def get(self, key: int) -> int:
        """
        Get the value of a key if it exists in the cache.
        Mark it as recently used by moving it to the head.
        
        Args:
            key: The key to look up
            
        Returns:
            The value associated with the key, or -1 if not found
        """
        if key not in self.cache:
            return -1
        
        node = self.cache[key]
        # Move the node to the head (mark as recently used)
        self._remove_node(node)
        self._add_to_head(node)
        
        return node.value
    
    def put(self, key: int, value: int) -> None:
        """
        Insert or update a key-value pair in the cache.
        If the cache exceeds capacity, evict the least recently used item.
        
        Args:
            key: The key to insert or update
            value: The value to associate with the key
        """
        if key in self.cache:
            # Update existing key
            node = self.cache[key]
            node.value = value
            # Move to head (mark as recently used)
            self._remove_node(node)
            self._add_to_head(node)
        else:
            # Add new key
            new_node = self.Node(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)
            
            # Check if we exceeded capacity
            if len(self.cache) > self.capacity:
                # Remove the least recently used item (right before tail)
                lru_node = self.tail.prev
                self._remove_node(lru_node)
                del self.cache[lru_node.key]
