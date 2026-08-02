class TrieNode:
    __slots__ = ("children", "is_word")

    def __init__(self):
        # children: mapping char -> TrieNode
        self.children = {}
        self.is_word = False


class Trie:
    """Simple Trie (prefix tree) implementation supporting insert, search, and starts_with."""

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Insert a word into the trie. Accepts empty string as a valid word."""
        if not isinstance(word, str):
            raise TypeError("word must be a string")
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_word = True

    def search(self, word: str) -> bool:
        """Return True if word is in the trie (exact match)."""
        if not isinstance(word, str):
            raise TypeError("word must be a string")
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_word

    def starts_with(self, prefix: str) -> bool:
        """Return True if there is any word in the trie that starts with the given prefix."""
        if not isinstance(prefix, str):
            raise TypeError("prefix must be a string")
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True
