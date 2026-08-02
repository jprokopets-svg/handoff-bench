
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

    num = 0
    while i < len(s) and s[i].isdigit():
        num = num * 10 + int(s[i])
        i += 1

    num *= sign

    MIN_INT = -2**31
    MAX_INT = 2**31 - 1

    if num < MIN_INT:
        return MIN_INT
    elif num > MAX_INT:
        return MAX_INT
    else:
        return num
