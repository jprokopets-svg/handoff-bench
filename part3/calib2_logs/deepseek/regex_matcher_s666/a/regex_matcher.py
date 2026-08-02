def full_match(pattern: str, text: str) -> bool:
    """Return True iff the entire text matches the pattern."""
    parser = Parser(pattern)
    try:
        ast = parser.parse()
    except ParseError as e:
        raise ValueError(str(e))
    matcher = Matcher(ast, text)
    return matcher.match()


class ParseError(Exception):
    pass


class Node:
    pass


class Literal(Node):
    __slots__ = ('ch',)
    def __init__(self, ch: str):
        self.ch = ch


class AnyChar(Node):
    pass


class CharClass(Node):
    __slots__ = ('negated', 'ranges')
    def __init__(self, negated: bool, ranges):
        self.negated = negated
        self.ranges = ranges  # list of (start, end) inclusive


class Group(Node):
    __slots__ = ('alternatives',)
    def __init__(self, alternatives):
        self.alternatives = alternatives  # list of list of Node


class Quantifier(Node):
    __slots__ = ('atom', 'min', 'max')
    def __init__(self, atom: Node, min_: int, max_: int):
        self.atom = atom
        self.min = min_  # 0 or 1
        self.max = max_  # None for unbounded


class AnchorStart(Node):
    pass


class AnchorEnd(Node):
    pass


class Parser:
    def __init__(self, pattern: str):
        self.pattern = pattern
        self.pos = 0
        self.length = len(pattern)

    def parse(self) -> list:
        """Parse pattern into a list of nodes."""
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
                self.pos += 1
                if self.pos >= self.length:
                    raise ParseError('unexpected end after backslash')
                esc = self.pattern[self.pos]
                # allowed escapes: any metacharacter
                nodes.append(Literal(esc))
                self.pos += 1
            elif ch == '.':
                nodes.append(AnyChar())
                self.pos += 1
            elif ch == '[':
                nodes.append(self.parse_char_class())
            elif ch == '(':
                nodes.append(self.parse_group())
            elif ch in '*+?':
                raise ParseError('quantifier without preceding atom')
            else:
                # literal character
                nodes.append(Literal(ch))
                self.pos += 1
            # after parsing an atom, check for quantifier
            if self.pos < self.length:
                ch = self.pattern[self.pos]
                if ch == '*':
                    atom = nodes[-1]
                    nodes[-1] = Quantifier(atom, 0, None)
                    self.pos += 1
                elif ch == '+':
                    atom = nodes[-1]
                    nodes[-1] = Quantifier(atom, 1, None)
                    self.pos += 1
                elif ch == '?':
                    atom = nodes[-1]
                    nodes[-1] = Quantifier(atom, 0, 1)
                    self.pos += 1
        return nodes

    def parse_char_class(self) -> CharClass:
        """Parse a character class starting at '['."""
        self.pos += 1  # skip '['
        if self.pos >= self.length:
            raise ParseError('unclosed character class')
        negated = False
        if self.pattern[self.pos] == '^':
            negated = True
            self.pos += 1
        ranges = []
        while self.pos < self.length:
            ch = self.pattern[self.pos]
            if ch == ']':
                self.pos += 1
                break
            # handle escape inside class
            if ch == '\\':
                self.pos += 1
                if self.pos >= self.length:
                    raise ParseError('unexpected end after backslash in class')
                esc = self.pattern[self.pos]
                start = esc
                self.pos += 1
            else:
                start = ch
                self.pos += 1
            # check for range
            if self.pos < self.length and self.pattern[self.pos] == '-':
                self.pos += 1
                if self.pos >= self.length:
                    raise ParseError('unexpected end in character class range')
                if self.pattern[self.pos] == ']':
                    # literal '-' at end of class
                    ranges.append((start, start))
                    ranges.append(('-', '-'))
                    continue
                # get end char
                if self.pattern[self.pos] == '\\':
                    self.pos += 1
                    if self.pos >= self.length:
                        raise ParseError('unexpected end after backslash in class')
                    end = self.pattern[self.pos]
                    self.pos += 1
                else:
                    end = self.pattern[self.pos]
                    self.pos += 1
                if ord(start) > ord(end):
                    raise ParseError('invalid range in character class')
                ranges.append((start, end))
            else:
                ranges.append((start, start))
        else:
            # loop ended without seeing ']'
            raise ParseError('unclosed character class')
        return CharClass(negated, ranges)

    def parse_group(self) -> Group:
        """Parse a group starting at '('."""
        self.pos += 1  # skip '('
        alternatives = []
        current = []
        while self.pos < self.length:
            ch = self.pattern[self.pos]
            if ch == ')':
                self.pos += 1
                if current:
                    alternatives.append(current)
                break
            elif ch == '|':
                alternatives.append(current)
                current = []
                self.pos += 1
            elif ch == '\\':
                self.pos += 1
                if self.pos >= self.length:
                    raise ParseError('unexpected end after backslash in group')
                esc = self.pattern[self.pos]
                current.append(Literal(esc))
                self.pos += 1
            elif ch == '.':
                current.append(AnyChar())
                self.pos += 1
            elif ch == '[':
                current.append(self.parse_char_class())
            elif ch == '(':
                current.append(self.parse_group())
            elif ch in '*+?':
                raise ParseError('quantifier without preceding atom')
            else:
                current.append(Literal(ch))
                self.pos += 1
            # check for quantifier after atom
            if self.pos < self.length:
                ch = self.pattern[self.pos]
                if ch == '*':
                    atom = current[-1]
                    current[-1] = Quantifier(atom, 0, None)
                    self.pos += 1
                elif ch == '+':
                    atom = current[-1]
                    current[-1] = Quantifier(atom, 1, None)
                    self.pos += 1
                elif ch == '?':
                    atom = current[-1]
                    current[-1] = Quantifier(atom, 0, 1)
                    self.pos += 1
        else:
            # loop ended without seeing ')'
            raise ParseError('unclosed group')
        return Group(alternatives)


class Matcher:
    def __init__(self, nodes: list, text: str):
        self.nodes = nodes
        self.text = text
        self.length = len(text)

    def match(self) -> bool:
        """Try to match nodes against entire text."""
        # Must match from start of text (position 0)
        consumed = self._match_from(0, self.nodes)
        if consumed is None:
            return False
        # Must have consumed entire text
        return consumed == self.length

    def _match_from(self, pos: int, nodes: list):
        """Try to match nodes starting at pos.
        Return number of characters consumed if successful, else None."""
        i = 0  # index in nodes
        p = pos  # position in text
        while i < len(nodes):
            node = nodes[i]
            if isinstance(node, AnchorStart):
                # Must be at start of whole text, not just current pos
                if p != 0:
                    return None
                i += 1
            elif isinstance(node, AnchorEnd):
                # Must be at end of whole text
                if p != self.length:
                    return None
                i += 1
            elif isinstance(node, Literal):
                if p >= self.length or self.text[p] != node.ch:
                    return None
                p += 1
                i += 1
            elif isinstance(node, AnyChar):
                if p >= self.length:
                    return None
                p += 1
                i += 1
            elif isinstance(node, CharClass):
                if p >= self.length:
                    return None
                ch = self.text[p]
                matched = False
                for start, end in node.ranges:
                    if start <= ch <= end:
                        matched = True
                        break
                if matched == node.negated:
                    return None
                p += 1
                i += 1
            elif isinstance(node, Group):
                # Try each alternative
                for alt in node.alternatives:
                    consumed = self._match_from(p, alt)
                    if consumed is not None:
                        p += consumed
                        i += 1
                        break
                else:
                    return None
            elif isinstance(node, Quantifier):
                # Greedy matching with backtracking
                atom = node.atom
                min_ = node.min
                max_ = node.max
                # First, match at least min_ times
                count = 0
                saved_p = p
                while count < min_:
                    consumed = self._match_one(p, atom)
                    if consumed is None:
                        # failed to match required minimum
                        return None
                    p += consumed
                    count += 1
                # Now match up to max_ times greedily
                matches = []
                while max_ is None or count < max_:
                    consumed = self._match_one(p, atom)
                    if consumed is None:
                        break
                    matches.append(consumed)
                    p += consumed
                    count += 1
                # Try to match the rest of nodes
                # Backtrack from most greedy to least
                for k in range(len(matches), -1, -1):
                    # k additional atoms beyond min_
                    # reset p to after min_ matches
                    trial_p = saved_p
                    for _ in range(min_ + k):
                        consumed = self._match_one(trial_p, atom)
                        trial_p += consumed
                    # try to match remaining nodes
                    rest_consumed = self._match_from(trial_p, nodes[i+1:])
                    if rest_consumed is not None:
                        # success
                        return (trial_p - pos) + rest_consumed
                # no backtracking succeeded
                return None
            else:
                raise RuntimeError(f'unknown node type {type(node)}')
        # All nodes matched
        return p - pos

    def _match_one(self, pos: int, node):
        """Match a single atom at pos. Return consumed count or None."""
        if isinstance(node, Literal):
            if pos >= self.length or self.text[pos] != node.ch:
                return None
            return 1
        elif isinstance(node, AnyChar):
            if pos >= self.length:
                return None
            return 1
        elif isinstance(node, CharClass):
            if pos >= self.length:
                return None
            ch = self.text[pos]
            matched = False
            for start, end in node.ranges:
                if start <= ch <= end:
                    matched = True
                    break
            if matched == node.negated:
                return None
            return 1
        elif isinstance(node, Group):
            # Try each alternative
            for alt in node.alternatives:
                consumed = self._match_from(pos, alt)
                if consumed is not None:
                    return consumed
            return None
        else:
            # Should not happen because quantifiers are expanded earlier
            raise RuntimeError(f'cannot match {type(node)} as single atom')