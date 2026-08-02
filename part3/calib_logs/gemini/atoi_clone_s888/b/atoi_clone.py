
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
        digit = int(s[i])
        result = result * 10 + digit
        i += 1

    # Clamp to 32-bit signed integer range
    INT_MAX = 2**31 - 1
    INT_MIN = -2**31

    result *= sign

    if result > INT_MAX:
        return INT_MAX
    if result < INT_MIN:
        return INT_MIN

    return result
