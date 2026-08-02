def my_atoi(s: str) -> int:
    """Convert string to 32-bit signed integer following rules:
    - skip leading whitespace
    - optional single '+' or '-' sign
    - read consecutive ASCII digits ('0'-'9') until non-digit
    - clamp to [-2**31, 2**31-1]
    - return 0 if no digits read
    """
    if not s:
        return 0
    i = 0
    n = len(s)
    # skip leading whitespace (use str.isspace() to cover common whitespace)
    while i < n and s[i].isspace():
        i += 1
    if i >= n:
        return 0
    # sign
    sign = 1
    if s[i] == '+':
        i += 1
    elif s[i] == '-':
        sign = -1
        i += 1
    # parse digits (only ASCII digits)
    value = 0
    digits_found = False
    INT_MAX = 2**31 - 1
    INT_MIN = -2**31
    while i < n:
        ch = s[i]
        if '0' <= ch <= '9':
            digits_found = True
            digit = ord(ch) - ord('0')
            # early overflow check
            if sign == 1:
                if value > (INT_MAX - digit) // 10:
                    return INT_MAX
            else:
                # for negative, compare with -(INT_MIN) == 2147483648
                if value > ((-INT_MIN) - digit) // 10:
                    return INT_MIN
            value = value * 10 + digit
            i += 1
        else:
            break
    if not digits_found:
        return 0
    result = sign * value
    # final clamp just in case
    if result < INT_MIN:
        return INT_MIN
    if result > INT_MAX:
        return INT_MAX
    return result
