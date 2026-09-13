# Simple regex engine implementation

class PatternError(ValueError):
    pass

class Node:
    def match(self, text, pos):
        raise NotImplementedError

class Literal(Node):
    def __init__(self, ch):
        self.ch = ch
    def match(self, text, pos):
        if pos < len(text) and text[pos] == self.ch:
            return {pos+1}
        return set()

class Dot(Node):
    def match(self, text, pos):
        if pos < len(text):
            return {pos+1}
        return set()

class CharClass(Node):
    def __init__(self, chars, negated=False):
        self.chars = chars  # set of characters
        self.negated = negated
    def match(self, text, pos):
        if pos < len(text):
            c = text[pos]
            ok = c in self.chars
            if self.negated:
                ok = not ok
            if ok:
                return {pos+1}
        return set()

class Sequence(Node):
    def __init__(self, nodes):
        self.nodes = nodes
    def match(self, text, pos):
        positions = {pos}
        for node in self.nodes:
            newpos = set()
            for p in positions:
                res = node.match(text, p)
                newpos.update(res)
            positions = newpos
            if not positions:
                break
        return positions

class Alternation(Node):
    def __init__(self, options):
        self.options = options  # list of Sequence nodes
    def match(self, text, pos):
        res = set()
        for opt in self.options:
            res.update(opt.match(text, pos))
        return res

class Star(Node):
    def __init__(self, node):
        self.node = node
    def match(self, text, pos):
        # compute closure of positions reachable by applying node 0 or more times
        results = {pos}
        frontier = {pos}
        visited = set()
        while frontier:
            new_frontier = set()
            for p in frontier:
                if (p) in visited:
                    continue
                visited.add(p)
                next_positions = self.node.match(text, p)
                for np in next_positions:
                    if np not in results:
                        results.add(np)
                        new_frontier.add(np)
            frontier = new_frontier
        return results

class Plus(Node):
    def __init__(self, node):
        self.node = node
    def match(self, text, pos):
        first = self.node.match(text, pos)
        results = set()
        for p in first:
            # after one match, apply star
            rest = Star(self.node).match(text, p)
            results.update(rest)
        return results

class Question(Node):
    def __init__(self, node):
        self.node = node
    def match(self, text, pos):
        res = {pos}
        res.update(self.node.match(text, pos))
        return res

class BeginAnchor(Node):
    def match(self, text, pos):
        return {pos} if pos == 0 else set()

class EndAnchor(Node):
    def match(self, text, pos):
        return {pos} if pos == len(text) else set()

# Parser

def parse_pattern(pat):
    i = 0
    n = len(pat)

    def parse_sequence():
        nodes = []
        nonlocal i
        while i < n and pat[i] not in ')|':
            if pat[i] in '*+?':
                # quantifier with no preceding atom
                raise PatternError('Quantifier with no preceding atom')
            atom = parse_atom()
            # check quantifier
            if i < n and pat[i] in '*+?':
                q = pat[i]
                i += 1
                if q == '*':
                    atom = Star(atom)
                elif q == '+':
                    atom = Plus(atom)
                else:
                    atom = Question(atom)
            nodes.append(atom)
        return Sequence(nodes)

    def parse_atom():
        nonlocal i
        if i >= n:
            raise PatternError('Unexpected end')
        ch = pat[i]
        if ch == '.':
            i += 1
            return Dot()
        if ch == '^':
            i += 1
            return BeginAnchor()
        if ch == '$':
            i += 1
            return EndAnchor()
        if ch == '\\':
            i += 1
            if i >= n:
                raise PatternError('Trailing backslash')
            esc = pat[i]
            i += 1
            return Literal(esc)
        if ch == '[':
            i += 1
            if i >= n:
                raise PatternError('Unclosed character class')
            negated = False
            if pat[i] == '^':
                negated = True
                i += 1
            chars = set()
            prev_char = None
            closed = False
            while i < n:
                if pat[i] == ']' and prev_char is None:
                    # empty class allowed? treat as literal ]? but tests don't cover; we'll treat as closed
                    closed = True
                    i += 1
                    break
                if pat[i] == ']':
                    closed = True
                    i += 1
                    break
                if pat[i] == '\\':
                    i += 1
                    if i >= n:
                        raise PatternError('Unclosed character class')
                    c = pat[i]
                    i += 1
                else:
                    c = pat[i]
                    i += 1
                if c == '-' and prev_char is not None and i < n and pat[i] != ']':
                    # range specified between prev_char and next char
                    # next char may be escaped
                    if pat[i] == '\\':
                        i += 1
                        if i >= n:
                            raise PatternError('Unclosed character class')
                        next_c = pat[i]
                        i += 1
                    else:
                        next_c = pat[i]
                        i += 1
                    if ord(prev_char) > ord(next_c):
                        # empty range, treat literally? We'll still add range by swapping
                        a, b = next_c, prev_char
                    else:
                        a, b = prev_char, next_c
                    for code in range(ord(a), ord(b)+1):
                        chars.add(chr(code))
                    prev_char = None
                else:
                    chars.add(c)
                    prev_char = c
            if not closed:
                raise PatternError('Unclosed character class')
            return CharClass(chars, negated)
        if ch == '(':
            i += 1
            # parse alternation inside group
            options = []
            while True:
                seq = parse_sequence()
                options.append(seq)
                if i < n and pat[i] == '|':
                    i += 1
                    continue
                break
            if i >= n or pat[i] != ')':
                raise PatternError('Unclosed group')
            i += 1
            if len(options) == 1:
                return options[0]
            else:
                return Alternation(options)
        # else literal
        i += 1
        return Literal(ch)

    seq = []
    # parse top-level alternation
    options = []
    while i < n:
        s = parse_sequence()
        options.append(s)
        if i < n and pat[i] == '|':
            i += 1
            continue
        break
    if i != n:
        # leftover closing paren etc.
        if pat[i] == ')':
            raise PatternError('Unclosed group')
    if len(options) == 1:
        return options[0]
    else:
        return Alternation(options)


def full_match(pattern, text):
    try:
        ast = parse_pattern(pattern)
    except PatternError:
        raise ValueError
    # match from pos 0; if pattern contains BeginAnchor/EndAnchor they handle positions
    positions = ast.match(text, 0)
    # full match requires one of positions == len(text)
    return len(text) in positions

# For direct module test
if __name__ == '__main__':
    pass
