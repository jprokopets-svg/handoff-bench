def full_match(pattern: str, text: str) -> bool:
    """
    Return True iff the entire text matches the pattern.
    """
    # Parse pattern into a list of tokens/instructions
    try:
        parser = Parser(pattern)
        ast = parser.parse()
    except ParseError as e:
        raise ValueError("malformed pattern") from e
    
    # Match the entire text
    return match_full(ast, text, 0, len(text)) == len(text)


class ParseError(Exception):
    pass


class Node:
    """AST node for regex."""
    pass


class Literal(Node):
    __slots__ = ('char',)
    def __init__(self, char: str):
        self.char = char


class AnyChar(Node):
    __slots__ = ()


class CharClass(Node):
    __slots__ = ('negated', 'ranges')
    def __init__(self, negated: bool, ranges):
        self.negated = negated
        self.ranges = ranges  # list of (start, end) inclusive


class Group(Node):
    __slots__ = ('alternatives',)
    def __init__(self, alternatives):
        self.alternatives = alternatives  # list of sequences of nodes


class Quantifier(Node):
    __slots__ = ('min', 'max', 'greedy', 'child')
    def __init__(self, child, min_, max_, greedy=True):
        self.child = child
        self.min = min_
        self.max = max_
        self.greedy = greedy


class AnchorStart(Node):
    __slots__ = ()


class AnchorEnd(Node):
    __slots__ = ()


class Parser:
    def __init__(self, pattern: str):
        self.pattern = pattern
        self.pos = 0
        self.length = len(pattern)
    
    def parse(self) -> list:
        """Parse whole pattern into a sequence of nodes."""
        nodes = []
        while self.pos < self.length:
            ch = self.pattern[self.pos]
            if ch == '^':
                nodes.append(AnchorStart())
                self.pos += 1
            elif ch == '$':
                nodes.append(AnchorEnd())
                self.pos += 1
            elif ch == '\\':
                nodes.append(self.parse_escape())
            elif ch == '[':
                nodes.append(self.parse_char_class())
            elif ch == '(':
                nodes.append(self.parse_group())
            elif ch == ')':
                # Should be handled inside parse_group
                raise ParseError("unmatched ')'")
            elif ch in '*+?':
                raise ParseError("quantifier without preceding atom")
            elif ch == '.':
                nodes.append(AnyChar())
                self.pos += 1
            elif ch == '|':
                raise ParseError("alternation without group")
            else:
                nodes.append(Literal(ch))
                self.pos += 1
            
            # Check for quantifier
            if self.pos < self.length:
                ch = self.pattern[self.pos]
                if ch in '*+?':
                    last = nodes[-1]
                    if isinstance(last, (AnchorStart, AnchorEnd)):
                        raise ParseError("quantifier on anchor")
                    nodes[-1] = self.parse_quantifier(last, ch)
    
        return nodes
    
    def parse_escape(self) -> Node:
        """Parse backslash escape."""
        self.pos += 1  # skip backslash
        if self.pos >= self.length:
            raise ParseError("unterminated escape")
        ch = self.pattern[self.pos]
        self.pos += 1
        # Escaped metacharacters: . * + ? \ [ ] ( ) ^ $ |
        if ch in '.\\*+?[]()^$|':
            return Literal(ch)
        # For simplicity, treat any other escaped char as literal
        return Literal(ch)
    
    def parse_char_class(self) -> Node:
        """Parse character class [...] or [^...]."""
        start_pos = self.pos
        self.pos += 1  # skip '['
        if self.pos >= self.length:
            raise ParseError("unclosed character class")
        
        negated = False
        if self.pattern[self.pos] == '^':
            negated = True
            self.pos += 1
        
        ranges = []
        while self.pos < self.length and self.pattern[self.pos] != ']':
            # Get start char
            if self.pattern[self.pos] == '\\':
                start = self.parse_escape_in_class()
            else:
                start = self.pattern[self.pos]
                self.pos += 1
            
            # Check for range
            if self.pos < self.length and self.pattern[self.pos] == '-':
                self.pos += 1
                if self.pos >= self.length or self.pattern[self.pos] == ']':
                    # dash at end of class, treat as literal dash
                    ranges.append((start, start))
                    ranges.append(('-', '-'))
                    continue
                # Get end char
                if self.pattern[self.pos] == '\\':
                    end = self.parse_escape_in_class()
                else:
                    end = self.pattern[self.pos]
                    self.pos += 1
                ranges.append((start, end))
            else:
                ranges.append((start, start))
        
        if self.pos >= self.length:
            raise ParseError("unclosed character class")
        # skip ']'
        self.pos += 1
        
        return CharClass(negated, ranges)
    
    def parse_escape_in_class(self) -> str:
        """Parse escape inside character class."""
        self.pos += 1  # skip backslash
        if self.pos >= self.length:
            raise ParseError("unterminated escape in class")
        ch = self.pattern[self.pos]
        self.pos += 1
        # Inside class, only \] \^ \- \\ need escaping?
        # Actually any metacharacter can be escaped, but we'll just return the char
        return ch
    
    def parse_group(self) -> Node:
        """Parse group (...) with possible alternation."""
        self.pos += 1  # skip '('
        alternatives = []
        current = []
        
        while self.pos < self.length:
            ch = self.pattern[self.pos]
            if ch == ')':
                self.pos += 1
                if current:
                    alternatives.append(current)
                if not alternatives:
                    alternatives.append([])  # empty group
                return Group(alternatives)
            elif ch == '|':
                alternatives.append(current)
                current = []
                self.pos += 1
            elif ch == '\\':
                current.append(self.parse_escape())
            elif ch == '[':
                current.append(self.parse_char_class())
            elif ch == '(':
                current.append(self.parse_group())
            elif ch == '.':
                current.append(AnyChar())
                self.pos += 1
            elif ch in '*+?':
                raise ParseError("quantifier without preceding atom")
            elif ch == '^':
                current.append(AnchorStart())
                self.pos += 1
            elif ch == '$':
                current.append(AnchorEnd())
                self.pos += 1
            else:
                current.append(Literal(ch))
                self.pos += 1
            
            # Check for quantifier
            if current and self.pos < self.length:
                ch = self.pattern[self.pos]
                if ch in '*+?':
                    last = current[-1]
                    if isinstance(last, (AnchorStart, AnchorEnd)):
                        raise ParseError("quantifier on anchor")
                    current[-1] = self.parse_quantifier(last, ch)
        
        raise ParseError("unclosed group")
    
    def parse_quantifier(self, child: Node, quant: str) -> Quantifier:
        """Parse quantifier * + ?."""
        self.pos += 1  # skip quant char
        if quant == '*':
            return Quantifier(child, 0, float('inf'))
        elif quant == '+':
            return Quantifier(child, 1, float('inf'))
        elif quant == '?':
            return Quantifier(child, 0, 1)
        else:
            raise ParseError(f"unknown quantifier {quant}")


def match_full(nodes: list, text: str, pos: int, end: int) -> int:
    """
    Try to match nodes against text[pos:end].
    Returns the new position if match succeeds, else -1.
    """
    # First, ensure start anchor at beginning
    if nodes and isinstance(nodes[0], AnchorStart):
        # Must match at start of text
        if pos != 0:
            return -1
        nodes = nodes[1:]
    
    # Process nodes
    result = match_sequence(nodes, text, pos, end)
    if result < 0:
        return -1
    
    # Check end anchor
    if result < end:
        # If there's an AnchorEnd at the end of nodes, we should have consumed it
        # Actually AnchorEnd is a node that matches end of text
        # Let's handle it during matching
        pass
    
    # Ensure we consumed entire text
    return result


def match_sequence(nodes: list, text: str, pos: int, end: int) -> int:
    """Match a sequence of nodes."""
    i = 0
    p = pos
    while i < len(nodes):
        node = nodes[i]
        if isinstance(node, AnchorEnd):
            # Must be at end of text
            if p != end:
                return -1
            i += 1
            continue
        # Try to match node
        new_p = match_node(node, text, p, end, nodes[i+1:])
        if new_p < 0:
            return -1
        p = new_p
        i += 1
    
    # If there's an implicit AnchorEnd at the end of pattern?
    # Actually full_match requires entire text to match, so we'll check later
    return p


def match_node(node: Node, text: str, pos: int, end: int, following: list) -> int:
    """Match a single node, with backtracking for quantifiers."""
    if isinstance(node, Literal):
        if pos < end and text[pos] == node.char:
            return pos + 1
        return -1
    elif isinstance(node, AnyChar):
        if pos < end:
            return pos + 1
        return -1
    elif isinstance(node, CharClass):
        if pos >= end:
            return -1
        ch = text[pos]
        matched = False
        for start, end_range in node.ranges:
            if start <= ch <= end_range:
                matched = True
                break
        if matched != node.negated:
            return pos + 1
        return -1
    elif isinstance(node, Group):
        # Try each alternative
        for alt in node.alternatives:
            # Combine alternative with following nodes
            new_p = match_sequence(alt + following, text, pos, end)
            if new_p >= 0:
                return new_p
        return -1
    elif isinstance(node, Quantifier):
        # Greedy matching with backtracking
        child = node.child
        min_ = node.min
        max_ = node.max
        
        # First, match at least min times
        p = pos
        count = 0
        while count < min_:
            new_p = match_node(child, text, p, end, [])
            if new_p < 0:
                return -1
            p = new_p
            count += 1
        
        # Now try to match as many as possible (greedy)
        matches = []
        while count < max_:
            new_p = match_node(child, text, p, end, [])
            if new_p < 0:
                break
            matches.append((p, new_p))
            p = new_p
            count += 1
        
        # Now try to match the following nodes
        # Start with the longest match and backtrack if needed
        for i in range(len(matches), -1, -1):
            if i == 0:
                current_pos = pos + (min_ * 0)  # actually we already matched min_
                # We need to compute position after matching min_ times
                # Let's recompute
                p0 = pos
                for _ in range(min_):
                    # We know these matches succeed
                    p0 = match_node(child, text, p0, end, [])
                test_pos = p0
            else:
                test_pos = matches[i-1][1]
            
            # Try to match following nodes
            new_p = match_sequence(following, text, test_pos, end)
            if new_p >= 0:
                return new_p
        
        return -1
    elif isinstance(node, AnchorStart):
        # Should have been handled earlier
        if pos == 0:
            return pos
        return -1
    elif isinstance(node, AnchorEnd):
        if pos == end:
            return pos
        return -1
    else:
        raise TypeError(f"unknown node type {type(node)}")


# For compatibility with test
if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        print(full_match(sys.argv[1], sys.argv[2]))