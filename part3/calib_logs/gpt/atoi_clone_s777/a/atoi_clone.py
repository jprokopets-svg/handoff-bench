def my_atoi(s: str) -> int:
    """Convert string to 32-bit signed integer following rules similar to C's atoi.

    - Skip leading whitespace
    - Optional '+' or '-' sign
    - Read digits until a non-digit
    - Clamp to 32-bit signed range
    - Return 0 if no digits were read
    """
    INT_MIN = -2**31
    INT_MAX = 2**31 - 1

    if not s:
        return 0

    i = 0
    n = len(s)
    # skip leading whitespace (spaces, tabs, newlines, etc.)
    while i < n and s[i].isspace():
        i += 1

    if i >= n:
        return 0

    sign = 1
    if s[i] == '+':
        sign = 1
        i += 1
    elif s[i] == '-':
        sign = -1
        i += 1

    # parse digits
    num = 0
    started = False
    while i < n and s[i].isdigit():
        started = True
        digit = ord(s[i]) - ord('0')
        num = num * 10 + digit
        # Early clamping to avoid overflow in Python (though Python int is unbounded)
        if sign == 1 and num > INT_MAX:
            return INT_MAX
        if sign == -1 and num > -INT_MIN:  # compare to 2147483648
            return INT_MIN
        i += 1

    if not started:
        return 0

    result = sign * num
    if result < INT_MIN:
        return INT_MIN
    if result > INT_MAX:
        return INT_MAX
    return result
