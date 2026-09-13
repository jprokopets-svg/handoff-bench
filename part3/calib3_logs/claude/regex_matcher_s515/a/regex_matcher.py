def full_match(pattern, text):
    """
    Returns True iff the ENTIRE text matches the pattern.
    Supported syntax:
    - Literal characters
    - '.' matches any single character
    - Character classes [abc], ranges [a-z], negation [^...]
    - Quantifiers: * (zero or more), + (one or more), ? (zero or one)
    - Groups (...) with alternation |
    - Anchors ^ (start) and $ (end)
    - Backslash escapes for metacharacters
    """
    try:
        parser = Parser(pattern)
        regex = parser.parse()
        return regex.match(text, 0) == len(text)
    except (ValueError, IndexError):
        raise ValueError("Malformed pattern")


class Parser:
    def __init__(self, pattern):
        self.pattern = pattern
        self.pos = 0
    
    def parse(self):
        """Parse the entire pattern into a regex tree."""
        return self.parse_alternation()
    
    def parse_alternation(self):
        """Parse alternation (lowest precedence): a|b|c"""
        left = self.parse_concatenation()
        
        if self.pos < len(self.pattern) and self.pattern[self.pos] == '|':
            alternatives = [left]
            while self.pos < len(self.pattern) and self.pattern[self.pos] == '|':
                self.pos += 1
                alternatives.append(self.parse_concatenation())
            return Alternation(alternatives)
        
        return left
    
    def parse_concatenation(self):
        """Parse concatenation: abc"""
        atoms = []
        
        while self.pos < len(self.pattern) and self.pattern[self.pos] not in '|)':
            atoms.append(self.parse_quantified())
        
        if not atoms:
            return Epsilon()
        if len(atoms) == 1:
            return atoms[0]
        return Concatenation(atoms)
    
    def parse_quantified(self):
        """Parse atom with optional quantifier."""
        atom = self.parse_atom()
        
        if self.pos < len(self.pattern) and self.pattern[self.pos] in '*+?':
            quantifier = self.pattern[self.pos]
            self.pos += 1
            
            if quantifier == '*':
                return Star(atom)
            elif quantifier == '+':
                return Plus(atom)
            elif quantifier == '?':
                return Optional(atom)
        
        return atom
    
    def parse_atom(self):
        """Parse a single atom: literal, dot, class, group, or anchor."""
        if self.pos >= len(self.pattern):
            raise ValueError("Unexpected end of pattern")
        
        ch = self.pattern[self.pos]
        
        # Anchor: ^
        if ch == '^':
            self.pos += 1
            return Anchor(True)
        
        # Anchor: $
        if ch == '$':
            self.pos += 1
            return Anchor(False)
        
        # Character class
        if ch == '[':
            return self.parse_class()
        
        # Group
        if ch == '(':
            self.pos += 1
            regex = self.parse_alternation()
            if self.pos >= len(self.pattern) or self.pattern[self.pos] != ')':
                raise ValueError("Unclosed group")
            self.pos += 1
            return Group(regex)
        
        # Quantifier without preceding atom
        if ch in '*+?':
            raise ValueError("Quantifier with no preceding atom")
        
        # Escape sequence
        if ch == '\\':
            self.pos += 1
            if self.pos >= len(self.pattern):
                raise ValueError("Incomplete escape sequence")
            escaped_ch = self.pattern[self.pos]
            self.pos += 1
            return Literal(escaped_ch)
        
        # Dot: any character
        if ch == '.':
            self.pos += 1
            return Dot()
        
        # Literal character
        self.pos += 1
        return Literal(ch)
    
    def parse_class(self):
        """Parse character class: [abc], [a-z], [^abc]"""
        self.pos += 1  # skip '['
        
        if self.pos >= len(self.pattern):
            raise ValueError("Unclosed character class")
        
        negated = False
        if self.pattern[self.pos] == '^':
            negated = True
            self.pos += 1
        
        chars = set()
        ranges = []
        
        while self.pos < len(self.pattern) and self.pattern[self.pos] != ']':
            ch = self.pattern[self.pos]
            
            # Escape sequence inside class
            if ch == '\\':
                self.pos += 1
                if self.pos >= len(self.pattern):
                    raise ValueError("Incomplete escape in character class")
                chars.add(self.pattern[self.pos])
                self.pos += 1
            else:
                # Check for range
                if self.pos + 2 < len(self.pattern) and self.pattern[self.pos + 1] == '-' and self.pattern[self.pos + 2] != ']':
                    start = ch
                    self.pos += 2
                    end = self.pattern[self.pos]
                    ranges.append((start, end))
                    self.pos += 1
                else:
                    chars.add(ch)
                    self.pos += 1
        
        if self.pos >= len(self.pattern):
            raise ValueError("Unclosed character class")
        
        self.pos += 1  # skip ']'
        
        return CharClass(chars, ranges, negated)


# Regex tree nodes

class Regex:
    """Base class for regex nodes."""
    def match(self, text, pos):
        """
        Try to match starting at position pos in text.
        Return the position after the match, or -1 if no match.
        """
        raise NotImplementedError


class Literal(Regex):
    def __init__(self, char):
        self.char = char
    
    def match(self, text, pos):
        if pos < len(text) and text[pos] == self.char:
            return pos + 1
        return -1


class Dot(Regex):
    def match(self, text, pos):
        if pos < len(text):
            return pos + 1
        return -1


class CharClass(Regex):
    def __init__(self, chars, ranges, negated):
        self.chars = chars
        self.ranges = ranges
        self.negated = negated
    
    def match(self, text, pos):
        if pos >= len(text):
            return -1
        
        ch = text[pos]
        matched = False
        
        # Check if in explicit chars
        if ch in self.chars:
            matched = True
        
        # Check if in ranges
        for start, end in self.ranges:
            if start <= ch <= end:
                matched = True
                break
        
        # Apply negation
        if self.negated:
            matched = not matched
        
        if matched:
            return pos + 1
        return -1


class Anchor(Regex):
    def __init__(self, is_start):
        self.is_start = is_start
    
    def match(self, text, pos):
        if self.is_start:
            # ^ matches at position 0
            if pos == 0:
                return pos
        else:
            # $ matches at end of text
            if pos == len(text):
                return pos
        return -1


class Epsilon(Regex):
    """Matches empty string."""
    def match(self, text, pos):
        return pos


class Group(Regex):
    def __init__(self, regex):
        self.regex = regex
    
    def match(self, text, pos):
        return self.regex.match(text, pos)


class Concatenation(Regex):
    def __init__(self, atoms):
        self.atoms = atoms
    
    def match(self, text, pos):
        for atom in self.atoms:
            result = atom.match(text, pos)
            if result == -1:
                return -1
            pos = result
        return pos


class Alternation(Regex):
    def __init__(self, alternatives):
        self.alternatives = alternatives
    
    def match(self, text, pos):
        for alt in self.alternatives:
            result = alt.match(text, pos)
            if result != -1:
                return result
        return -1


class Star(Regex):
    """Zero or more: greedy with backtracking."""
    def __init__(self, atom):
        self.atom = atom
    
    def match(self, text, pos):
        # Try to match as many times as possible (greedy)
        positions = [pos]
        current_pos = pos
        
        while True:
            result = self.atom.match(text, current_pos)
            if result == -1:
                break
            positions.append(result)
            current_pos = result
        
        # Try positions from longest to shortest (backtracking)
        for try_pos in reversed(positions):
            yield_pos = try_pos
            return yield_pos
        
        return -1


class Plus(Regex):
    """One or more: greedy with backtracking."""
    def __init__(self, atom):
        self.atom = atom
    
    def match(self, text, pos):
        # Must match at least once
        result = self.atom.match(text, pos)
        if result == -1:
            return -1
        
        # Then try to match more (greedy)
        positions = [result]
        current_pos = result
        
        while True:
            next_result = self.atom.match(text, current_pos)
            if next_result == -1:
                break
            positions.append(next_result)
            current_pos = next_result
        
        # Return the longest match
        return positions[-1]


class Optional(Regex):
    """Zero or one."""
    def __init__(self, atom):
        self.atom = atom
    
    def match(self, text, pos):
        result = self.atom.match(text, pos)
        if result != -1:
            return result
        return pos
