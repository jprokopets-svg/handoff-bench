def my_atoi(s: str) -> int:
    """
    Convert a string to a 32-bit signed integer.
    
    Rules:
    1. Skip leading whitespace
    2. Accept an optional sign (+ or -)
    3. Read digits until a non-digit is encountered
    4. Clamp to 32-bit signed range [-2147483648, 2147483647]
    5. Return 0 if no digits are read
    """
    # 32-bit signed integer bounds
    INT_MAX = 2147483647
    INT_MIN = -2147483648
    
    # Skip leading whitespace
    i = 0
    while i < len(s) and s[i] == ' ':
        i += 1
    
    # Check for sign
    sign = 1
    if i < len(s) and s[i] in ['+', '-']:
        if s[i] == '-':
            sign = -1
        i += 1
    
    # Read digits
    result = 0
    while i < len(s) and s[i].isdigit():
        digit = int(s[i])
        result = result * 10 + digit
        i += 1
    
    # Apply sign
    result = sign * result
    
    # Clamp to 32-bit signed range
    if result > INT_MAX:
        result = INT_MAX
    elif result < INT_MIN:
        result = INT_MIN
    
    return result
