class TrieNode:
    """A node in the Trie data structure."""
    def __init__(self):
        self.children = {}  # Dictionary mapping character to TrieNode
        self.is_end_of_word = False  # Flag indicating if this node marks the end of a word


class Trie:
    """A Trie (prefix tree) data structure for efficient string storage and retrieval."""
    
    def __init__(self):
        """Initialize the Trie with a root node."""
        self.root = TrieNode()
    
    def insert(self, word: str) -> None:
        """Insert a word into the Trie.
        
        Args:
            word: The word to insert.
        """
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
    
    def search(self, word: str) -> bool:
        """Search for an exact word in the Trie.
        
        Args:
            word: The word to search for.
            
        Returns:
            True if the word exists in the Trie, False otherwise.
        """
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word
    
    def starts_with(self, prefix: str) -> bool:
        """Check if any word in the Trie starts with the given prefix.
        
        Args:
            prefix: The prefix to check.
            
        Returns:
            True if any word starts with the prefix, False otherwise.
        """
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True
