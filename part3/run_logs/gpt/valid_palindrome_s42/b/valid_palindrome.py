def valid_palindrome(s: str) -> bool:
    """Return True if s is a palindrome ignoring non-alphanumeric characters and case.

    If s is None, treat it as a palindrome (consistent with previous behavior).
    """
    if s is None:
        return True
    i, j = 0, len(s) - 1
    while i < j:
        # move i forward to next alphanumeric
        while i < j and not s[i].isalnum():
            i += 1
        # move j backward to previous alphanumeric
        while i < j and not s[j].isalnum():
            j -= 1
        if i < j:
            if s[i].lower() != s[j].lower():
                return False
            i += 1
            j -= 1
    return True
