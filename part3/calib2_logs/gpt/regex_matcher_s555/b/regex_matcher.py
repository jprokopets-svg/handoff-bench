import re


def full_match(pattern: str, text: str) -> bool:
    """Return True iff the entire text matches the given pattern.

    Convert re.error into ValueError for malformed patterns.
    """
    try:
        prog = re.compile(pattern)
    except re.error as e:
        raise ValueError(str(e))
    return prog.fullmatch(text) is not None
