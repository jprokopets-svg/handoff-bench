def my_atoi(s: str) -> int:
    # 32-bit signed integer bounds
    INT_MAX = 2147483647
    INT_MIN = -2147483648
    
    # Step 1: Skip leading whitespace
    i = 0
    while i < len(s) and s[i] == ' ':
        i += 1
    
    # Step 2: Check for optional sign
    sign = 1
    if i < len(s) and s[i] in ['+', '-']:
        if s[i] == '-':
            sign = -1
        i += 1
    
    # Step 3: Read digits until non-digit encountered
    result = 0
    while i < len(s) and s[i].isdigit():
        digit = int(s[i])
        result = result * 10 + digit
        i += 1
    
    # Step 4: Apply sign
    result = sign * result
    
    # Step 5: Clamp to 32-bit signed integer range
    if result > INT_MAX:
        return INT_MAX
    if result < INT_MIN:
        return INT_MIN
    
    return result
