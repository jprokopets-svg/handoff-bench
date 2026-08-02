def my_atoi(s: str) -> int:
    # Edge case: empty string
    if not s:
        return 0
    
    i = 0
    n = len(s)
    
    # 1. Skip leading whitespace
    while i < n and s[i] == ' ':
        i += 1
    
    # Edge case: all whitespace or end of string
    if i == n:
        return 0
    
    # 2. Check for sign
    sign = 1
    if s[i] == '+':
        i += 1
    elif s[i] == '-':
        sign = -1
        i += 1
    
    # Edge case: no digits after sign
    if i == n or not s[i].isdigit():
        return 0
    
    # 3. Read digits until non-digit
    result = 0
    int_min = -2147483648
    int_max = 2147483647
    
    while i < n and s[i].isdigit():
        digit = ord(s[i]) - ord('0')
        
        # Check for overflow before multiplying
        if result > (int_max - digit) // 10:
            return int_max if sign == 1 else int_min
        
        result = result * 10 + digit
        i += 1
    
    # Apply sign and return
    return sign * result