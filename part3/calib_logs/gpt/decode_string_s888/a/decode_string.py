def decode_string(s: str) -> str:
    """Decode string with pattern k[encoded_string], supports nesting."""
    if not s:
        return ""
    num_stack = []
    str_stack = []
    current_num = 0
    current_str = ""
    for ch in s:
        if ch.isdigit():
            current_num = current_num * 10 + int(ch)
        elif ch == '[':
            # push current context
            num_stack.append(current_num)
            str_stack.append(current_str)
            current_num = 0
            current_str = ""
        elif ch == ']':
            if not num_stack:
                # unmatched bracket, treat literally (or ignore)
                continue
            repeat = num_stack.pop()
            prev_str = str_stack.pop()
            current_str = prev_str + current_str * repeat
        else:
            current_str += ch
    return current_str
