import re


def full_match(pattern: str, text: str) -> bool:
    """Return True iff the entire text matches the given regex pattern.

    This implementation delegates to Python's `re` module. Malformed patterns
    (as detected by re.compile) raise ValueError.
    """
    try:
        prog = re.compile(pattern)
    except re.error as e:
        raise ValueError(str(e))
    return prog.fullmatch(text) is not None
