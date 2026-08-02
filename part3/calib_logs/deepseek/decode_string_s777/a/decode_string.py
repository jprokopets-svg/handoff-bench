def decode_string(s: str) -> str:
    stack = []
    current_num = 0
    current_str = ""
    
    for char in s:
        if char.isdigit():
            current_num = current_num * 10 + int(char)
        elif char == '[':
            # Push current number and string to stack
            stack.append((current_num, current_str))
            current_num = 0
            current_str = ""
        elif char == ']':
            # Pop from stack and decode
            num, prev_str = stack.pop()
            current_str = prev_str + current_str * num
        else:
            # Regular character
            current_str += char
    
    return current_str