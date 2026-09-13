def full_match(pattern: str, text: str) -> bool:
    # Parse pattern into a tree of operations
    # We'll use a recursive descent parser
    
    # First, check for anchors
    start_anchor = pattern.startswith('^')
    end_anchor = pattern.endswith('$')
    if start_anchor:
        pattern = pattern[1:]
    if end_anchor:
        pattern = pattern[:-1]
    
    # Parse pattern into a sequence of atoms with quantifiers
    parsed = parse_pattern(pattern)
    
    # Match function with backtracking
    def match(pos: int, text_pos: int) -> bool:
        # If we consumed all atoms
        if pos == len(parsed):
            # If we also consumed all text, success
            return text_pos == len(text)
        
        atom, quantifier = parsed[pos]
        
        # Helper to try matching the atom at text_pos
        def matches_atom(at_pos):
            if at_pos >= len(text):
                return False
            return atom_matches(atom, text[at_pos])
        
        # Handle quantifiers
        if quantifier == '?':
            # Zero or one
            # Try skipping (zero)
            if match(pos + 1, text_pos):
                return True
            # Try matching one
            if matches_atom(text_pos) and match(pos + 1, text_pos + 1):
                return True
            return False
        
        elif quantifier == '*':
            # Zero or more - greedy with backtracking
            # First try matching as many as possible
            count = 0
            while text_pos + count < len(text) and matches_atom(text_pos + count):
                count += 1
            
            # Try decreasing count from max down to 0
            for c in range(count, -1, -1):
                if match(pos + 1, text_pos + c):
                    return True
            return False
        
        elif quantifier == '+':
            # One or more - greedy with backtracking
            # Must match at least one
            count = 0
            while text_pos + count < len(text) and matches_atom(text_pos + count):
                count += 1
            
            if count == 0:
                return False
            
            # Try decreasing count from max down to 1
            for c in range(count, 0, -1):
                if match(pos + 1, text_pos + c):
                    return True
            return False
        
        else:
            # No quantifier, match exactly one
            if not matches_atom(text_pos):
                return False
            return match(pos + 1, text_pos + 1)
    
    # Try all possible starting positions if no start anchor
    if start_anchor:
        # Must match from beginning
        return match(0, 0)
    else:
        # Can match anywhere, but must consume entire text (due to full_match)
        # Actually full_match means entire text must match pattern,
        # but without ^ anchor we can start anywhere? 
        # The test 'a$' with 'ba' returns False, meaning 'a$' must match at end
        # but 'a' doesn't match 'ba' because 'a' is not at end? Wait test says:
        # assert full_match('a$', 'ba') == False
        # 'a$' means 'a' at end of text. 'ba' ends with 'a', so should match?
        # Actually 'ba' ends with 'a', so 'a$' should match 'ba'? Let me re-read.
        # The test says assert full_match('a$', 'ba') == False
        # That means 'a$' does NOT match 'ba'. So 'a$' requires the entire text to be 'a'
        # not just ending with 'a'. Because full_match means entire text matches pattern.
        # So anchors ^ and $ are redundant with full_match? Actually ^ means start of text,
        # $ means end of text. In full_match, pattern must match entire text, so ^ and $
        # are implicitly there? But they allow explicit anchors.
        # For simplicity, we'll treat full_match as requiring pattern to match entire text.
        # So we just need to check if match(0, 0) succeeds.
        # However, without start anchor, we still need to match from beginning of text
        # because full_match means entire text must be consumed.
        # Actually the pattern 'a' should match text 'a' but not 'ba' because 'ba' has extra 'b'.
        # So we need to match from start of text and consume all text.
        # So we can just call match(0, 0) regardless of anchors?
        # But anchors affect internal matching: ^ forces start, $ forces end.
        # Since we're doing full_match, we always need to match from pos 0 to end.
        # However, pattern '^a' should match 'a' but not 'ba' (because 'ba' doesn't start with 'a').
        # Actually 'ba' doesn't start with 'a', so match(0,0) would fail anyway.
        # Let's implement: if start_anchor, we must match from text pos 0.
        # if not start_anchor, we can try any starting position? But we must consume all text.
        # That means we need to find some starting position where pattern matches and consumes rest.
        # But full_match means entire text matches pattern, not that pattern matches a substring.
        # So pattern must match from beginning to end of text. So start_anchor is implicit.
        # However, test 'a$' with 'ba' fails, meaning 'a$' doesn't match 'ba' even though
        # 'ba' ends with 'a'. So 'a$' requires text to be exactly 'a', not ending with 'a'.
        # That's because $ anchor means end of text, and we're matching entire text.
        # So we should treat pattern as anchored at both ends for full_match.
        # Actually the spec says anchors ^ and $ are supported. In full_match context,
        # they're redundant but allowed.
        # Let's implement by always requiring match to start at text position 0 and end at len(text).
        # The anchors just affect internal matching of start/end positions.
        # So we'll just call match(0, 0) and require it to reach end.
        # The match function already checks if we consumed all atoms and all text.
        # So we can just:
        return match(0, 0)

def parse_pattern(pattern: str):
    """Parse pattern into list of (atom, quantifier) pairs.
    Atom can be: char, '.', charclass, group (list of alternatives).
    Raises ValueError on malformed pattern.
    """
    pos = 0
    result = []
    
    while pos < len(pattern):
        ch = pattern[pos]
        
        if ch == '\\':
            # Escape sequence
            if pos + 1 >= len(pattern):
                raise ValueError("Incomplete escape sequence")
            nxt = pattern[pos + 1]
            # Valid escape: any metacharacter
            atom = ('escaped', nxt)
            pos += 2
        elif ch == '.':
            atom = ('any',)
            pos += 1
        elif ch == '[':
            # Character class
            class_end = pos + 1
            negated = False
            if class_end < len(pattern) and pattern[class_end] == '^':
                negated = True
                class_end += 1
            
            # Parse class contents
            class_chars = []
            while class_end < len(pattern) and pattern[class_end] != ']':
                if pattern[class_end] == '\\':
                    # Escaped character in class
                    if class_end + 1 >= len(pattern):
                        raise ValueError("Incomplete escape in character class")
                    class_chars.append(pattern[class_end + 1])
                    class_end += 2
                else:
                    class_chars.append(pattern[class_end])
                    class_end += 1
            
            if class_end >= len(pattern):
                raise ValueError("Unclosed character class")
            
            # Now class_chars may contain ranges like 'a-z'
            # Process ranges
            expanded = set()
            i = 0
            while i < len(class_chars):
                if i + 2 < len(class_chars) and class_chars[i + 1] == '-':
                    # Range a-z
                    start = class_chars[i]
                    end = class_chars[i + 2]
                    if start > end:
                        raise ValueError("Invalid range in character class")
                    for c in range(ord(start), ord(end) + 1):
                        expanded.add(chr(c))
                    i += 3
                else:
                    expanded.add(class_chars[i])
                    i += 1
            
            atom = ('class', expanded, negated)
            pos = class_end + 1
        elif ch == '(':
            # Group
            group_end = pos + 1
            depth = 1
            while group_end < len(pattern) and depth > 0:
                if pattern[group_end] == '\\':
                    group_end += 2
                    continue
                if pattern[group_end] == '(':
                    depth += 1
                elif pattern[group_end] == ')':
                    depth -= 1
                group_end += 1
            
            if depth > 0:
                raise ValueError("Unclosed group")
            
            # Extract group content (without parentheses)
            group_content = pattern[pos + 1:group_end - 1]
            # Parse alternatives
            alternatives = parse_alternatives(group_content)
            atom = ('group', alternatives)
            pos = group_end
        elif ch in ')|':
            # These should only appear inside groups
            raise ValueError("Unexpected character")
        else:
            # Literal character
            atom = ('char', ch)
            pos += 1
        
        # Check for quantifier
        quantifier = None
        if pos < len(pattern) and pattern[pos] in '*+?':
            quantifier = pattern[pos]
            pos += 1
        
        result.append((atom, quantifier))
    
    return result

def parse_alternatives(pattern: str):
    """Parse pattern containing | alternations."""
    parts = []
    start = 0
    depth = 0
    for i, ch in enumerate(pattern):
        if ch == '\\':
            i += 1  # Skip escaped char
            continue
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
        elif ch == '|' and depth == 0:
            parts.append(pattern[start:i])
            start = i + 1
    
    parts.append(pattern[start:])
    return [parse_pattern(part) for part in parts]

def atom_matches(atom, ch: str) -> bool:
    """Check if atom matches character ch."""
    atom_type = atom[0]
    if atom_type == 'char':
        return atom[1] == ch
    elif atom_type == 'any':
        return True
    elif atom_type == 'escaped':
        # Escaped metacharacter matches literally
        return atom[1] == ch
    elif atom_type == 'class':
        _, chars, negated = atom
        in_class = ch in chars
        return not in_class if negated else in_class
    elif atom_type == 'group':
        # Group matches if any alternative matches at this position
        # But groups are handled differently in match function
        # Actually groups are expanded as sequences of atoms
        # So atom_matches shouldn't be called for groups
        raise RuntimeError("Group should not be in atom_matches")
    else:
        raise RuntimeError(f"Unknown atom type {atom_type}")

# The match function needs to handle groups
# Let's rewrite the full_match with proper group handling

# Actually, we need to redesign: groups are sequences of atoms themselves.
# So we should flatten groups into the parsing.
# Let me rewrite parse_pattern to handle groups differently.

# But due to time, let's implement a simpler approach: compile pattern to NFA.
# However, given complexity, I'll implement a backtracking matcher that parses on the fly.

# Let me rewrite from scratch with a cleaner design.