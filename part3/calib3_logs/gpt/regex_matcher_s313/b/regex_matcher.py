from typing import Set, List


class PatternError(ValueError):
    pass


class Node:
    def match(self, text: str, pos: int) -> Set[int]:
        raise NotImplementedError


class Literal(Node):
    def __init__(self, ch: str):
        self.ch = ch

    def match(self, text, pos):
        if pos < len(text) and text[pos] == self.ch:
            return {pos + 1}
        return set()


class Dot(Node):
    def match(self, text, pos):
        if pos < len(text):
            return {pos + 1}
        return set()


class CharClass(Node):
    def __init__(self, chars: Set[str], neg: bool = False):
        self.chars = set(chars)
        self.neg = neg

    def match(self, text, pos):
        if pos < len(text):
            c = text[pos]
            inside = c in self.chars
            if self.neg:
                if not inside:
                    return {pos + 1}
            else:
                if inside:
                    return {pos + 1}
        return set()


class Sequence(Node):
    def __init__(self, nodes: List[Node]):
        self.nodes = nodes

    def match(self, text, pos):
        positions = {pos}
        for node in self.nodes:
            newpos = set()
            for p in positions:
                newpos.update(node.match(text, p))
            positions = newpos
            if not positions:
                return set()
        return positions


class Alternation(Node):
    def __init__(self, options: List[Node]):
        self.options = options

    def match(self, text, pos):
        out = set()
        for opt in self.options:
            out.update(opt.match(text, pos))
        return out


class Star(Node):
    def __init__(self, node: Node):
        self.node = node

    def match(self, text, pos):
        # closure: allow zero or more repeats; avoid infinite loops by requiring progress
        results = set()
        stack = [pos]
        visited = set([pos])
        results.add(pos)
        while stack:
            cur = stack.pop()
            for nxt in self.node.match(text, cur):
                if nxt not in visited and nxt > cur:
                    visited.add(nxt)
                    results.add(nxt)
                    stack.append(nxt)
        return results


class Plus(Node):
    def __init__(self, node: Node):
        self.node = node

    def match(self, text, pos):
        first = self.node.match(text, pos)
        out = set()
        for p in first:
            # from each first-match position, apply star semantics
            out.update(Star(self.node).match(text, p))
        return out


class Question(Node):
    def __init__(self, node: Node):
        self.node = node

    def match(self, text, pos):
        out = {pos}
        out.update(self.node.match(text, pos))
        return out


class BeginAnchor(Node):
    def match(self, text, pos):
        if pos == 0:
            return {pos}
        return set()


class EndAnchor(Node):
    def match(self, text, pos):
        if pos == len(text):
            return {pos}
        return set()


def parse_pattern(pat: str) -> Node:
    i = 0
    n = len(pat)

    def parse_alternation() -> Node:
        nonlocal i
        options = [parse_sequence()]
        while i < n and pat[i] == '|':
            i += 1
            options.append(parse_sequence())
        if len(options) == 1:
            return options[0]
        return Alternation(options)

    def parse_sequence() -> Node:
        nonlocal i
        nodes: List[Node] = []
        while i < n and pat[i] not in ')|':
            node = parse_atom()
            if node is None:
                break
            # handle quantifiers
            if i < n and pat[i] in '*+?':
                q = pat[i]
                i += 1
                if q == '*':
                    node = Star(node)
                elif q == '+':
                    node = Plus(node)
                else:
                    node = Question(node)
            nodes.append(node)
        if not nodes:
            return Sequence([])
        if len(nodes) == 1:
            return nodes[0]
        return Sequence(nodes)

    def parse_atom() -> Node:
        nonlocal i
        if i >= n:
            return None
        c = pat[i]
        # anchors
        if c == '^':
            i += 1
            return BeginAnchor()
        if c == '$':
            i += 1
            return EndAnchor()
        if c == '.':
            i += 1
            return Dot()
        if c == '(':
            i += 1
            if i <= n and pat[i - 1] == '(':
                # parse group
                node = parse_alternation()
                if i >= n or pat[i] != ')':
                    raise PatternError('Unclosed group')
                i += 1
                return node
        if c == '[':
            i += 1
            if i >= n:
                raise PatternError('Unclosed character class')
            neg = False
            if pat[i] == '^':
                neg = True
                i += 1
            chars = set()
            first_in_class = True
            while i < n and pat[i] != ']':
                ch = pat[i]
                if ch == '\':
                    i += 1
                    if i >= n:
                        raise PatternError('Bad escape in class')
                    ch = pat[i]
                    chars.add(ch)
                    i += 1
                    first_in_class = False
                    continue
                # range handling
                if i + 2 < n and pat[i + 1] == '-' and pat[i + 2] != ']':
                    start = pat[i]
                    end = pat[i + 2]
                    # consume three chars
                    i += 3
                    if ord(start) <= ord(end):
                        rng = (chr(c) for c in range(ord(start), ord(end) + 1))
                    else:
                        rng = (chr(c) for c in range(ord(end), ord(start) + 1))
                    chars.update(rng)
                    first_in_class = False
                    continue
                else:
                    chars.add(ch)
                    i += 1
                    first_in_class = False
            if i >= n or pat[i] != ']':
                raise PatternError('Unclosed character class')
            i += 1
            if not chars:
                # empty class matches nothing
                return CharClass(set(), False)
            return CharClass(chars, neg)
        if c == '\':
            i += 1
            if i >= n:
                raise PatternError('Trailing backslash')
            ch = pat[i]
            i += 1
            return Literal(ch)
        # literal
        if c in '*+?':
            # quantifier without atom
            raise PatternError('Quantifier with no preceding atom')
        # normal literal
        i += 1
        return Literal(c)

    node = parse_alternation()
    if i != n:
        raise PatternError('Malformed pattern')
    return node


def full_match(pattern: str, text: str) -> bool:
    try:
        node = parse_pattern(pattern)
    except PatternError as e:
        raise ValueError(str(e))
    positions = node.match(text, 0)
    return len(text) in positions
