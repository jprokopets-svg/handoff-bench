def my_atoi(s: str) -> int:
    """
    Convert string to 32-bit signed integer.
    
    Steps:
    1. Skip leading whitespace
    2. Check for optional sign (+ or -)
    3. Read digits until non-digit character
    4. Convert to integer
    5. Clamp to [-2147483648, 2147483647]
    6. Return 0 if no digits read
    """
    if not s:
        return 0
    
    # Skip leading whitespace
    i = 0
    n = len(s)
    while i < n and s[i] == ' ':
        i += 1
    
    if i >= n:
        return 0
    
    # Check for sign
    sign = 1
    if s[i] == '-':
        sign = -1
        i += 1
    elif s[i] == '+':
        i += 1
    
    # Read digits
    result = 0
    while i < n and s[i].isdigit():
        digit = ord(s[i]) - ord('0')
        # Check for overflow before multiplying
        if result > (2147483647 - digit) // 10:
            return 2147483647 if sign == 1 else -2147483648
        result = result * 10 + digit
        i += 1
    
    # Apply sign and clamp
    result *= sign
    if result > 2147483647:
        return 2147483647
    if result < -2147483648:
        return -2147483648
    
    return result