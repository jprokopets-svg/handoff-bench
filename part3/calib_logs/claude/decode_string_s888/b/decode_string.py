def decode_string(s: str) -> str:
    """
    Decodes an encoded string of the form k[encoded_string].
    
    Args:
        s: An encoded string where k is a positive integer and the content repeats k times.
           Nesting is allowed.
    
    Returns:
        The decoded string.
    
    Examples:
        '3[a]2[bc]' -> 'aaabcbc'
        '3[a2[c]]' -> 'accaccacc'
        '2[abc]3[cd]ef' -> 'abcabccdcdcdef'
    """
    stack = []
    current_num = 0
    current_str = ""
    
    for char in s:
        if char.isdigit():
            # Build multi-digit numbers
            current_num = current_num * 10 + int(char)
        elif char == '[':
            # Push current state to stack and reset for nested content
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
