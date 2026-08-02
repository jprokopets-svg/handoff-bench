from typing import List, Optional, Tuple, Union

class Node:
    """Base class for regex nodes"""
    pass

class Literal(Node):
    def __init__(self, char: str):
        self.char = char
    
    def __repr__(self):
        return f"Literal('{self.char}')"

class AnyChar(Node):
    def __repr__(self):
        return "AnyChar()"

class CharClass(Node):
    def __init__(self, negated: bool, ranges: List[Tuple[str, str]]):
        self.negated = negated
        self.ranges = ranges  # list of (start, end) inclusive ranges
    
    def __repr__(self):
        return f"CharClass(negated={self.negated}, ranges={self.ranges})"

class Quantifier(Node):
    def __init__(self, node: Node, min_count: int, max_count: Optional[int]):
        self.node = node
        self.min_count = min_count  # 0 or 1
        self.max_count = max_count  # None for unlimited
    
    def __repr__(self):
        max_str = "inf" if self.max_count is None else self.max_count
        return f"Quantifier(node={self.node}, min={self.min_count}, max={max_str})"

class Group(Node):
    def __init__(self, nodes: List[Node]):
        self.nodes = nodes
    
    def __repr__(self):
        return f"Group({self.nodes})"

class Alternation(Node):
    def __init__(self, left: List[Node], right: List[Node]):
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"Alternation(left={self.left}, right={self.right})"

class AnchorStart(Node):
    def __repr__(self):
        return "AnchorStart()"

class AnchorEnd(Node):
    def __repr__(self):
        return "AnchorEnd()"

class Parser:
    def __init__(self, pattern: str):
        self.pattern = pattern
        self.pos = 0
        self.length = len(pattern)
    
    def parse(self) -> List[Node]:
        """Parse the entire pattern into a list of nodes"""
        nodes = []
        while self.pos < self.length:
            node = self.parse_atom()
            if node is None:
                break
            nodes.append(node)
        return nodes
    
    def parse_atom(self) -> Optional[Node]:
        """Parse a single atom (literal, ., char class, group, anchor, escape)"""
        if self.pos >= self.length:
            return None
        
        ch = self.pattern[self.pos]
        
        if ch == '^':
            self.pos += 1
            return AnchorStart()
        elif ch == '$':
            self.pos += 1
            return AnchorEnd()
        elif ch == '.':
            self.pos += 1
            return AnyChar()
        elif ch == '[':
            return self.parse_char_class()
        elif ch == '(':
            return self.parse_group()
        elif ch == '\\':
            return self.parse_escape()
        elif ch in '*+?':
            raise ValueError("Quantifier without preceding atom")
        elif ch == ')':
            # End of group, handled by parse_group
            return None
        elif ch == '|':
            # Alternation, handled by parse_group
            return None
        else:
            # Literal character
            self.pos += 1
            return Literal(ch)
    
    def parse_char_class(self) -> CharClass:
        """Parse a character class: [abc], [a-z], [^...]"""
        self.pos += 1  # Skip '['
        if self.pos >= self.length:
            raise ValueError("Unclosed character class")
        
        negated = False
        if self.pattern[self.pos] == '^':
            negated = True
            self.pos += 1
        
        ranges = []
        while self.pos < self.length and self.pattern[self.pos] != ']':
            start = self.parse_char_class_char()
            
            if self.pos < self.length - 1 and self.pattern[self.pos] == '-':
                # It's a range
                self.pos += 1  # Skip '-'
                if self.pos >= self.length or self.pattern[self.pos] == ']':
                    # Range at end, treat '-' as literal
                    ranges.append((start, start))
                    ranges.append(('-', '-'))
                    continue
                end = self.parse_char_class_char()
                if ord(start) > ord(end):
                    raise ValueError("Invalid range in character class")
                ranges.append((start, end))
            else:
                # Single character
                ranges.append((start, start))
        
        if self.pos >= self.length:
            raise ValueError("Unclosed character class")
        
        self.pos += 1  # Skip ']'
        return CharClass(negated, ranges)
    
    def parse_char_class_char(self) -> str:
        """Parse a single character inside a character class, handling escapes"""
        if self.pos >= self.length:
            raise ValueError("Unclosed character class")
        
        ch = self.pattern[self.pos]
        if ch == '\\':
            self.pos += 1
            if self.pos >= self.length:
                raise ValueError("Incomplete escape in character class")
            ch = self.pattern[self.pos]
            self.pos += 1
            return ch
        else:
            self.pos += 1
            return ch
    
    def parse_group(self) -> Node:
        """Parse a group: (pattern) or alternation (a|b)"""
        self.pos += 1  # Skip '('
        
        # Parse left side
        left_nodes = []
        while self.pos < self.length and self.pattern[self.pos] != '|' and self.pattern[self.pos] != ')':
            node = self.parse_atom()
            if node is None:
                break
            left_nodes.append(node)
        
        if self.pos >= self.length:
            raise ValueError("Unclosed group")
        
        if self.pattern[self.pos] == '|':
            # Alternation
            self.pos += 1  # Skip '|'
            
            # Parse right side
            right_nodes = []
            while self.pos < self.length and self.pattern[self.pos] != ')':
                node = self.parse_atom()
                if node is None:
                    break
                right_nodes.append(node)
            
            if self.pos >= self.length:
                raise ValueError("Unclosed group")
            
            self.pos += 1  # Skip ')'
            return Alternation(left_nodes, right_nodes)
        else:
            # Simple group
            self.pos += 1  # Skip ')'
            return Group(left_nodes)
    
    def parse_escape(self) -> Node:
        """Parse an escaped character: \., \*, \\, etc."""
        self.pos += 1  # Skip '\\'
        if self.pos >= self.length:
            raise ValueError("Incomplete escape sequence")
        
        ch = self.pattern[self.pos]
        self.pos += 1
        
        # Escaped metacharacters become literals
        if ch in '.\\*+?^$[]()|':
            return Literal(ch)
        else:
            # Any other escaped character is just the character itself
            return Literal(ch)
    
    def apply_quantifier(self, node: Node) -> Node:
        """Apply quantifier (*, +, ?) to the preceding node if present"""
        if self.pos >= self.length:
            return node
        
        ch = self.pattern[self.pos]
        if ch == '*':
            self.pos += 1
            return Quantifier(node, 0, None)
        elif ch == '+':
            self.pos += 1
            return Quantifier(node, 1, None)
        elif ch == '?':
            self.pos += 1
            return Quantifier(node, 0, 1)
        else:
            return node
    
    def parse_with_quantifiers(self) -> List[Node]:
        """Parse pattern with quantifiers applied to atoms"""
        nodes = []
        while self.pos < self.length:
            node = self.parse_atom()
            if node is None:
                break
            
            # Apply quantifier if present
            node = self.apply_quantifier(node)
            nodes.append(node)
        
        return nodes


class Matcher:
    def __init__(self, nodes: List[Node]):
        self.nodes = nodes
    
    def match(self, text: str, full: bool = True) -> bool:
        """Match text against the pattern"""
        # For full_match, we must match from position 0 and consume all characters
        result = self._match_from(text, 0, 0)
        if result is None:
            return False
        # Must have consumed all characters
        return result == len(text)
    
    def _match_from(self, text: str, text_pos: int, node_idx: int) -> Optional[int]:
        """Try to match from text_pos and node_idx, return final text position if successful"""
        if node_idx == len(self.nodes):
            return text_pos
        
        node = self.nodes[node_idx]
        
        if isinstance(node, AnchorStart):
            if text_pos != 0:
                return None
            return self._match_from(text, text_pos, node_idx + 1)
        
        elif isinstance(node, AnchorEnd):
            if text_pos != len(text):
                return None
            return self._match_from(text, text_pos, node_idx + 1)
        
        elif isinstance(node, Literal):
            if text_pos < len(text) and text[text_pos] == node.char:
                return self._match_from(text, text_pos + 1, node_idx + 1)
            return None
        
        elif isinstance(node, AnyChar):
            if text_pos < len(text):
                return self._match_from(text, text_pos + 1, node_idx + 1)
            return None
        
        elif isinstance(node, CharClass):
            if text_pos >= len(text):
                return None
            
            ch = text[text_pos]
            matched = False
            
            for start, end in node.ranges:
                if start <= ch <= end:
                    matched = True
                    break
            
            if node.negated:
                matched = not matched
            
            if matched:
                return self._match_from(text, text_pos + 1, node_idx + 1)
            return None
        
        elif isinstance(node, Group):
            # Group is just a sequence of nodes
            # Create a temporary matcher for the group
            group_matcher = Matcher(node.nodes)
            result = group_matcher._match_from(text, text_pos, 0)
            if result is not None:
                return self._match_from(text, result, node_idx + 1)
            return None
        
        elif isinstance(node, Alternation):
            # Try left branch
            left_matcher = Matcher(node.left)
            result = left_matcher._match_from(text, text_pos, 0)
            if result is not None:
                final = self._match_from(text, result, node_idx + 1)
                if final is not None:
                    return final
            
            # Try right branch
            right_matcher = Matcher(node.right)
            result = right_matcher._match_from(text, text_pos, 0)
            if result is not None:
                return self._match_from(text, result, node_idx + 1)
            return None
        
        elif isinstance(node, Quantifier):
            # Greedy matching with backtracking
            min_count = node.min_count
            max_count = node.max_count
            
            # Try from max possible down to min
            if max_count is None:
                # Unlimited, start with as many as possible
                max_try = len(text) - text_pos + 1
            else:
                max_try = min(max_count, len(text) - text_pos + 1)
            
            # Try decreasing number of repetitions
            for count in range(max_try, min_count - 1, -1):
                # Try to match 'count' repetitions
                current_pos = text_pos
                success = True
                
                for _ in range(count):
                    # Match one repetition
                    if isinstance(node.node, Literal):
                        if current_pos < len(text) and text[current_pos] == node.node.char:
                            current_pos += 1
                        else:
                            success = False
                            break
                    elif isinstance(node.node, AnyChar):
                        if current_pos < len(text):
                            current_pos += 1
                        else:
                            success = False
                            break
                    elif isinstance(node.node, CharClass):
                        if current_pos >= len(text):
                            success = False
                            break
                        
                        ch = text[current_pos]
                        matched = False
                        for start, end in node.node.ranges:
                            if start <= ch <= end:
                                matched = True
                                break
                        
                        if node.node.negated:
                            matched = not matched
                        
                        if matched:
                            current_pos += 1
                        else:
                            success = False
                            break
                    elif isinstance(node.node, Group):
                        group_matcher = Matcher(node.node.nodes)
                        result = group_matcher._match_from(text, current_pos, 0)
                        if result is not None:
                            current_pos = result
                        else:
                            success = False
                            break
                    elif isinstance(node.node, Alternation):
                        # For alternation inside quantifier, we need to handle it
                        # Create a matcher for the alternation node
                        alt_matcher = Matcher([node.node])
                        result = alt_matcher._match_from(text, current_pos, 0)
                        if result is not None:
                            current_pos = result
                        else:
                            success = False
                            break
                    else:
                        # Shouldn't happen
                        success = False
                        break
                
                if success:
                    # Try to match the rest of the pattern
                    result = self._match_from(text, current_pos, node_idx + 1)
                    if result is not None:
                        return result
            
            return None
        
        else:
            # Unknown node type
            return None


def full_match(pattern: str, text: str) -> bool:
    """Return True iff the ENTIRE text matches the pattern."""
    # Parse the pattern
    parser = Parser(pattern)
    try:
        nodes = parser.parse_with_quantifiers()
    except ValueError as e:
        raise ValueError(f"Malformed pattern: {