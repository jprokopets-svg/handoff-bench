def decode_string(s: str) -> str:
    """
    Decode an encoded string with nested repetition patterns.
    
    Format: k[encoded_string] where k is a positive integer.
    Supports multi-digit numbers and arbitrary nesting depth.
    
    Examples:
        '3[a]' -> 'aaa'
        '3[a2[c]]' -> 'accaccacc'
        '2[abc]3[cd]ef' -> 'abcabccdcdcdef'
    
    Args:
        s: Encoded string
        
    Returns:
        Decoded string
    """
    stack = []
    current_num = 0
    current_str = ""
    
    for char in s:
        if char.isdigit():
            # Build multi-digit numbers
            current_num = current_num * 10 + int(char)
        elif char == '[':
            # Push current state onto stack and reset for nested content
            stack.append((current_str, current_num))
            current_str = ""
            current_num = 0
        elif char == ']':
            # Pop from stack and apply repetition
            prev_str, num = stack.pop()
            current_str = prev_str + current_str * num
        else:
            # Regular character
            current_str += char
    
    return current_str
