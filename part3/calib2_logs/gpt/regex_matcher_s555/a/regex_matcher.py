import re


def full_match(pattern, text):
    """Return True iff the ENTIRE text matches the pattern.

    This implementation uses Python's re engine for matching and relies on
    re.compile to detect malformed patterns (raising re.error), which we
    convert to ValueError as required by the specification.
    """
    try:
        prog = re.compile(pattern)
    except re.error as e:
        raise ValueError(str(e))
    return prog.fullmatch(text) is not None
