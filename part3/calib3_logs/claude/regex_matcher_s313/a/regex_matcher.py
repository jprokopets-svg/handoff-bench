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
        parsed = parse_pattern(pattern)
        return match_pattern(parsed, text, 0, 0) == len(text)
    except ValueError:
        raise


def parse_pattern(pattern):
    """Parse pattern string into an AST."""
    tokens, pos = parse_alternation(pattern, 0)
    if pos != len(pattern):
        raise ValueError(f"Unexpected character at position {pos}")
    return tokens


def parse_alternation(pattern, pos):
    """Parse alternation (lowest precedence): a|b|c"""
    left, pos = parse_sequence(pattern, pos)
    
    if pos < len(pattern) and pattern[pos] == '|':
        alternatives = [left]
        while pos < len(pattern) and pattern[pos] == '|':
            pos += 1
            right, pos = parse_sequence(pattern, pos)
            alternatives.append(right)
        return ('alternation', alternatives), pos
    
    return left, pos


def parse_sequence(pattern, pos):
    """Parse sequence of atoms with quantifiers."""
    atoms = []
    
    while pos < len(pattern) and pattern[pos] not in '|)':
        atom, pos = parse_atom(pattern, pos)
        
        # Check for quantifier
        if pos < len(pattern) and pattern[pos] in '*+?':
            quantifier = pattern[pos]
            pos += 1
            atom = ('quantifier', quantifier, atom)
        
        atoms.append(atom)
    
    if len(atoms) == 0:
        return ('sequence', []), pos
    elif len(atoms) == 1:
        return atoms[0], pos
    else:
        return ('sequence', atoms), pos


def parse_atom(pattern, pos):
    """Parse a single atom (literal, dot, class, group, or anchor)."""
    if pos >= len(pattern):
        raise ValueError("Unexpected end of pattern")
    
    ch = pattern[pos]
    
    if ch == '^':
        return ('anchor', '^'), pos + 1
    elif ch == '$':
        return ('anchor', '$'), pos + 1
    elif ch == '.':
        return ('dot',), pos + 1
    elif ch == '[':
        return parse_class(pattern, pos)
    elif ch == '(':
        return parse_group(pattern, pos)
    elif ch == '\\':
        return parse_escape(pattern, pos)
    elif ch in '*+?)':
        raise ValueError(f"Quantifier '{ch}' with no preceding atom")
    else:
        return ('literal', ch), pos + 1


def parse_escape(pattern, pos):
    """Parse escaped character."""
    if pos + 1 >= len(pattern):
        raise ValueError("Incomplete escape sequence")
    
    next_ch = pattern[pos + 1]
    return ('literal', next_ch), pos + 2


def parse_class(pattern, pos):
    """Parse character class [abc], [a-z], [^abc]."""
    if pos >= len(pattern) or pattern[pos] != '[':
        raise ValueError("Expected '['")
    
    pos += 1
    negated = False
    
    if pos < len(pattern) and pattern[pos] == '^':
        negated = True
        pos += 1
    
    ranges = []
    
    while pos < len(pattern) and pattern[pos] != ']':
        if pattern[pos] == '\\':
            # Escaped character in class
            if pos + 1 >= len(pattern):
                raise ValueError("Incomplete escape in character class")
            ch = pattern[pos + 1]
            pos += 2
            ranges.append(('char', ch))
        else:
            ch = pattern[pos]
            pos += 1
            
            # Check for range
            if pos < len(pattern) and pattern[pos] == '-' and pos + 1 < len(pattern) and pattern[pos + 1] != ']':
                pos += 1  # consume '-'
                end_ch = pattern[pos]
                pos += 1
                ranges.append(('range', ch, end_ch))
            else:
                ranges.append(('char', ch))
    
    if pos >= len(pattern):
        raise ValueError("Unclosed character class")
    
    pos += 1  # consume ']'
    
    return ('class', negated, ranges), pos


def parse_group(pattern, pos):
    """Parse group (...)."""
    if pos >= len(pattern) or pattern[pos] != '(':
        raise ValueError("Expected '('")
    
    pos += 1
    inner, pos = parse_alternation(pattern, pos)
    
    if pos >= len(pattern) or pattern[pos] != ')':
        raise ValueError("Unclosed group")
    
    pos += 1
    return ('group', inner), pos


def match_pattern(parsed, text, text_pos, depth=0):
    """
    Match pattern against text starting at text_pos.
    Returns the position in text after matching, or -1 if no match.
    """
    if isinstance(parsed, tuple):
        if parsed[0] == 'literal':
            if text_pos < len(text) and text[text_pos] == parsed[1]:
                return text_pos + 1
            return -1
        
        elif parsed[0] == 'dot':
            if text_pos < len(text):
                return text_pos + 1
            return -1
        
        elif parsed[0] == 'anchor':
            if parsed[1] == '^':
                return text_pos if text_pos == 0 else -1
            elif parsed[1] == '$':
                return text_pos if text_pos == len(text) else -1
        
        elif parsed[0] == 'class':
            if text_pos >= len(text):
                return -1
            ch = text[text_pos]
            negated, ranges = parsed[1], parsed[2]
            matches = char_in_class(ch, ranges)
            if matches != negated:
                return text_pos + 1
            return -1
        
        elif parsed[0] == 'sequence':
            pos = text_pos
            for atom in parsed[1]:
                result = match_pattern(atom, text, pos, depth + 1)
                if result == -1:
                    return -1
                pos = result
            return pos
        
        elif parsed[0] == 'quantifier':
            quantifier, atom = parsed[1], parsed[2]
            return match_quantifier(quantifier, atom, text, text_pos, depth + 1)
        
        elif parsed[0] == 'group':
            return match_pattern(parsed[1], text, text_pos, depth + 1)
        
        elif parsed[0] == 'alternation':
            for alternative in parsed[1]:
                result = match_pattern(alternative, text, text_pos, depth + 1)
                if result != -1:
                    return result
            return -1
    
    return -1


def match_quantifier(quantifier, atom, text, text_pos, depth):
    """Match quantified atom with backtracking."""
    if quantifier == '*':
        # Zero or more: try greedy first, then backtrack
        return match_greedy(atom, text, text_pos, 0, None, depth)
    elif quantifier == '+':
        # One or more: must match at least once
        result = match_pattern(atom, text, text_pos, depth)
        if result == -1:
            return -1
        return match_greedy(atom, text, result, 1, None, depth)
    elif quantifier == '?':
        # Zero or one: try matching first, then no match
        result = match_pattern(atom, text, text_pos, depth)
        if result != -1:
            return result
        return text_pos
    
    return -1


def match_greedy(atom, text, text_pos, count, min_count, depth):
    """
    Greedy matching with backtracking.
    Try to match as many times as possible, then backtrack if needed.
    """
    # Try to match one more time
    result = match_pattern(atom, text, text_pos, depth)
    
    if result != -1 and result > text_pos:
        # Successfully matched, try to match more
        further = match_greedy(atom, text, result, count + 1, min_count, depth)
        if further != -1:
            return further
        # Backtrack: return current position
        return result
    
    # Can't match more, return current position
    return text_pos


def char_in_class(ch, ranges):
    """Check if character is in the given ranges."""
    for item in ranges:
        if item[0] == 'char':
            if ch == item[1]:
                return True
        elif item[0] == 'range':
            start, end = item[1], item[2]
            if ord(start) <= ord(ch) <= ord(end):
                return True
    return False
