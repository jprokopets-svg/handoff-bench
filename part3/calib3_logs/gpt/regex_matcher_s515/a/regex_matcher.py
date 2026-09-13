import re


def full_match(pattern: str, text: str) -> bool:
    """Return True iff entire text matches the pattern.

    This implementation delegates to Python's re module. It translates the
    behavior required by the tests directly to re.fullmatch. Malformed
    patterns (unclosed groups/classes or quantifier with no atom) cause
    re.error which is converted to ValueError per the problem statement.
    """
    try:
        # Try compiling to detect malformed patterns
        compiled = re.compile(pattern)
    except re.error as e:
        raise ValueError(str(e))
    return compiled.fullmatch(text) is not None
