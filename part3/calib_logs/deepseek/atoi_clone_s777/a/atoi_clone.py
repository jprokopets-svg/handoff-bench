def my_atoi(s: str) -> int:
    """
    Convert string to 32-bit signed integer.
    
    Steps:
    1. Skip leading whitespace
    2. Check for optional sign (+ or -)
    3. Read digits until non-digit character
    4. Convert digits to integer
    5. Apply sign
    6. Clamp to 32-bit signed range [-2147483648, 2147483647]
    7. Return 0 if no digits read
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
    digits = []
    while i < n and s[i].isdigit():
        digits.append(s[i])
        i += 1
    
    if not digits:
        return 0
    
    # Convert to integer
    result = 0
    for digit in digits:
        result = result * 10 + (ord(digit) - ord('0'))
    
    # Apply sign
    result *= sign
    
    # Clamp to 32-bit signed range
    INT_MIN = -2147483648
    INT_MAX = 2147483647
    
    if result < INT_MIN:
        return INT_MIN
    if result > INT_MAX:
        return INT_MAX
    
    return result