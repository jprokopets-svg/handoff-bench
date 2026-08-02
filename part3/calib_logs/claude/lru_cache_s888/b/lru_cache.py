class Node:
    """Node in the doubly-linked list"""
    def __init__(self, key: int = 0, value: int = 0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    """
    LRU Cache implementation using doubly-linked list + hash map.
    
    - get(key): O(1) average time - returns value or -1 if absent
    - put(key, value): O(1) average time - inserts/updates and evicts LRU when full
    """
    
    def __init__(self, capacity: int):
        """Initialize cache with given capacity"""
        self.capacity = capacity
        self.cache = {}  # key -> Node mapping for O(1) lookups
        
        # Dummy head and tail nodes to simplify edge cases
        self.head = Node()  # Most recently used end
        self.tail = Node()  # Least recently used end
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def get(self, key: int) -> int:
        """
        Get value for key. Returns -1 if key not found.
        Marks the key as recently used.
        """
        if key not in self.cache:
            return -1
        
        node = self.cache[key]
        # Move node to head (most recently used)
        self._remove_node(node)
        self._add_to_head(node)
        return node.value
    
    def put(self, key: int, value: int) -> None:
        """
        Insert or update key-value pair.
        Evicts least recently used item if capacity exceeded.
        """
        if key in self.cache:
            # Update existing node
            node = self.cache[key]
            node.value = value
            # Move to head (most recently used)
            self._remove_node(node)
            self._add_to_head(node)
        else:
            # Create new node
            node = Node(key, value)
            self.cache[key] = node
            self._add_to_head(node)
            
            # Check capacity and evict if necessary
            if len(self.cache) > self.capacity:
                # Remove least recently used (node before tail)
                lru_node = self.tail.prev
                self._remove_node(lru_node)
                del self.cache[lru_node.key]
    
    def _remove_node(self, node: Node) -> None:
        """Remove node from doubly-linked list"""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node
    
    def _add_to_head(self, node: Node) -> None:
        """Add node right after head (most recently used position)"""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
