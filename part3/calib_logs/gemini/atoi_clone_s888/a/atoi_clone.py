
def my_atoi(s: str) -> int:
    s = s.strip()
    if not s:
        return 0

    sign = 1
    i = 0
    if s[0] == '-':
        sign = -1
        i += 1
    elif s[0] == '+':
        i += 1

    result = 0
    while i < len(s) and s[i].isdigit():
        result = result * 10 + int(s[i])
        i += 1

    result *= sign

    # Clamp to 32-bit signed integer range
    INT_MAX = 2**31 - 1
    INT_MIN = -2**31

    if result > INT_MAX:
        return INT_MAX
    elif result < INT_MIN:
        return INT_MIN
    else:
        return result
