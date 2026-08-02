class Trie:
    def __init__(self):
        self.root = {}
        self.end_symbol = "*"
    
    def insert(self, word: str) -> None:
        """Inserts a word into the trie."""
        node = self.root
        for char in word:
            if char not in node:
                node[char] = {}
            node = node[char]
        node[self.end_symbol] = True
    
    def search(self, word: str) -> bool:
        """Returns True if the word is in the trie."""
        node = self.root
        for char in word:
            if char not in node:
                return False
            node = node[char]
        return self.end_symbol in node
    
    def starts_with(self, prefix: str) -> bool:
        """Returns True if there is any word in the trie that starts with the given prefix."""
        node = self.root
        for char in prefix:
            if char not in node:
                return False
            node = node[char]
        return True