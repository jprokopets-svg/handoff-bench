def my_atoi(s: str) -> int:
    # Edge case: empty string
    if not s:
        return 0
    
    # Skip leading whitespace
    i = 0
    while i < len(s) and s[i] == ' ':
        i += 1
    
    # Check if we reached the end of string
    if i >= len(s):
        return 0
    
    # Check for sign
    sign = 1
    if s[i] == '-':
        sign = -1
        i += 1
    elif s[i] == '+':
        i += 1
    
    # Parse digits
    result = 0
    while i < len(s) and s[i].isdigit():
        digit = int(s[i])
        
        # Check for overflow before adding the digit
        # For positive numbers
        if sign == 1:
            if result > 214748364 or (result == 214748364 and digit > 7):
                return 2147483647
        # For negative numbers
        else:
            if result > 214748364 or (result == 214748364 and digit > 8):
                return -2147483648
        
        result = result * 10 + digit
        i += 1
    
    return sign * result