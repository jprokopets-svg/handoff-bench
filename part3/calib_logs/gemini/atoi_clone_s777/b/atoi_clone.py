
def my_atoi(s: str) -> int:
    i = 0
    n = len(s)
    sign = 1
    result = 0
    
    # Skip leading whitespace
    while i < n and s[i] == ' ':
        i += 1
        
    # Check for sign
    if i < n and (s[i] == '+' or s[i] == '-'):
        if s[i] == '-':
            sign = -1
        i += 1
        
    # Convert digits
    while i < n and s[i].isdigit():
        digit = int(s[i])
        
        # Check for overflow/underflow before multiplication
        if sign == 1:
            if result > (2**31 - 1 - digit) // 10:
                return 2**31 - 1
        else: # sign == -1
            if result > (2**31 - digit) // 10:
                return -2**31
                
        result = result * 10 + digit
        i += 1
        
    result = result * sign
    
    # Clamp to 32-bit signed integer range
    if result > 2**31 - 1:
        return 2**31 - 1
    elif result < -2**31:
        return -2**31
    else:
        return result
