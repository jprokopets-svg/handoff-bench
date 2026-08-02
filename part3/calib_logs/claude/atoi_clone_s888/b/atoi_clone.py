def my_atoi(s: str) -> int:
    """
    Convert a string to a 32-bit signed integer.
    
    Rules:
    - Skip leading whitespace
    - Accept optional '+' or '-' sign
    - Read digits until a non-digit character
    - Clamp result to 32-bit signed range [-2147483648, 2147483647]
    - Return 0 if no valid digits are found
    """
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
    
    # Step 3: Read digits and accumulate result
    result = 0
    while i < len(s) and s[i].isdigit():
        digit = int(s[i])
        
        # Check for overflow before accumulating
        # If result > INT_MAX // 10, or result == INT_MAX // 10 and digit > 7,
        # then result * 10 + digit would overflow
        if result > INT_MAX // 10 or (result == INT_MAX // 10 and digit > 7):
            # Overflow detected
            return INT_MAX if sign == 1 else INT_MIN
        
        result = result * 10 + digit
        i += 1
    
    # Step 4: Apply sign and clamp to 32-bit range
    result = sign * result
    result = max(INT_MIN, min(INT_MAX, result))
    
    return result
