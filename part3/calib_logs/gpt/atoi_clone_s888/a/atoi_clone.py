INT_MAX = 2**31 - 1
INT_MIN = -2**31

def my_atoi(s: str) -> int:
    """Convert string to 32-bit signed integer (clamped).

    Behaves like C's atoi / LeetCode String to Integer (atoi).
    """
    if s is None:
        return 0
    i = 0
    n = len(s)
    # skip leading whitespace
    while i < n and s[i].isspace():
        i += 1
    if i >= n:
        return 0
    # sign
    sign = 1
    if s[i] == '+':
        sign = 1
        i += 1
    elif s[i] == '-':
        sign = -1
        i += 1
    # read digits
    num = 0
    started = False
    while i < n and s[i].isdigit():
        started = True
        digit = ord(s[i]) - ord('0')
        # check overflow before adding
        if sign == 1:
            if num > (INT_MAX - digit) // 10:
                return INT_MAX
        else:
            # for negative, allow up to INT_MAX+1
            if num > ((-INT_MIN) - digit) // 10:
                return INT_MIN
        num = num * 10 + digit
        i += 1
    if not started:
        return 0
    result = sign * num
    # final clamp just in case
    if result < INT_MIN:
        return INT_MIN
    if result > INT_MAX:
        return INT_MAX
    return result


if __name__ == "__main__":
    # quick manual test
    print(my_atoi('42'))
