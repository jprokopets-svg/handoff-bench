def my_atoi(s: str) -> int:
    """Convert a string to a 32-bit signed integer similar to C's atoi.

    Rules implemented:
    - Skip leading whitespace
    - Optional '+' or '-' sign
    - Read consecutive ASCII digits [0-9]
    - Stop at first non-digit after digits begin
    - If no digits read, return 0
    - Clamp to 32-bit signed integer range [-2**31, 2**31 - 1]
    """
    INT_MAX = 2**31 - 1
    INT_MIN = -2**31

    if s is None:
        return 0
    if not isinstance(s, str):
        # If input isn't a string, we don't attempt complex coercion; return 0
        return 0

    i = 0
    n = len(s)
    # skip leading whitespace
    while i < n and s[i].isspace():
        i += 1

    # optional sign
    sign = 1
    if i < n and (s[i] == '+' or s[i] == '-'):
        if s[i] == '-':
            sign = -1
        i += 1

    result = 0
    digits_found = False
    while i < n:
        ch = s[i]
        # only accept ASCII digits 0-9
        if ch < '0' or ch > '9':
            break
        digits_found = True
        digit = ord(ch) - ord('0')
        # check overflow before multiplying by 10
        if result > (INT_MAX - digit) // 10:
            return INT_MAX if sign == 1 else INT_MIN
        result = result * 10 + digit
        i += 1

    if not digits_found:
        return 0

    return sign * result
