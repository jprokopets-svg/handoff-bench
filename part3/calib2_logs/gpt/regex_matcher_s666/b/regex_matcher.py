import re


def full_match(pattern: str, text: str) -> bool:
    """Return True iff the entire text matches the given regex pattern.

    Malformed patterns (e.g., unclosed group, class, or stray quantifier)
    raise ValueError.
    """
    try:
        prog = re.compile(pattern)
    except re.error as e:
        raise ValueError(str(e))
    # Use fullmatch semantics: entire string must match
    return prog.fullmatch(text) is not None
