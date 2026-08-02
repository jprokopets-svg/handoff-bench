import re


def full_match(pattern: str, text: str) -> bool:
    """
    Return True iff the ENTIRE text matches the pattern.
    Uses Python's re to perform matching; converts re.error to ValueError for malformed patterns.
    """
    try:
        # Compile to detect malformed patterns (unclosed groups/classes, nothing to repeat, etc.)
        prog = re.compile(pattern)
    except re.error as e:
        raise ValueError(str(e))
    # Use fullmatch to ensure entire text is matched
    m = prog.fullmatch(text)
    return m is not None
