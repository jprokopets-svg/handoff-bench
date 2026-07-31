def is_match(s: str, p: str) -> bool:
    """
    Determines if string `s` matches pattern `p`.

    Pattern rules:
      '.' matches any single character.
      '*' matches zero or more of the preceding character.

    Args:
        s: The input string to test.
        p: The pattern string.

    Returns:
        True if the entire string matches the pattern, False otherwise.
    """
    # Base case: empty pattern
    if not p:
        return not s

    # Check if the first character matches
    first_match = bool(s) and p[0] in (s[0], '.')

    # If the next character in pattern is '*'
    if len(p) >= 2 and p[1] == '*':
        # Two choices:
        # 1. Skip the "x*" part (zero occurrences)
        # 2. Use one occurrence of the preceding char (if it matches)
        return is_match(s, p[2:]) or (first_match and is_match(s[1:], p))
    else:
        # No '*', must match first char and continue
        return first_match and is_match(s[1:], p[1:])
