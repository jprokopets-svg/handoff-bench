def decode_string(s: str) -> str:
    """
    Decode an encoded string of the form k[encoded_string].
    
    Args:
        s: The encoded string
        
    Returns:
        The decoded string
    """
    stack = []
    current_num = 0
    current_str = ''
    
    for char in s:
        if char.isdigit():
            current_num = current_num * 10 + int(char)
        elif char == '[':
            # Push current context to stack
            stack.append((current_str, current_num))
            current_str = ''
            current_num = 0
        elif char == ']':
            # Pop from stack and build the string
            prev_str, num = stack.pop()
            current_str = prev_str + current_str * num
        else:
            # Regular character
            current_str += char
    
    return current_str