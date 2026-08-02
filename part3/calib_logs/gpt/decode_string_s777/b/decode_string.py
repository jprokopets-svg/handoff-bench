def decode_string(s: str) -> str:
    """Decode an encoded string with format k[encoded_string].

    Supports nested brackets and multi-digit repeat counts.
    """
    if not s:
        return ''

    count_stack = []
    string_stack = []
    current_num = 0
    current_str = ''

    for ch in s:
        if ch.isdigit():
            # build multi-digit number
            current_num = current_num * 10 + int(ch)
        elif ch == '[':
            # push current context and reset
            string_stack.append(current_str)
            count_stack.append(current_num)
            current_str = ''
            current_num = 0
        elif ch == ']':
            # pop and build new string
            if count_stack:
                repeat = count_stack.pop()
            else:
                # malformed input: treat as literal
                repeat = 1
            if string_stack:
                prev = string_stack.pop()
            else:
                prev = ''
            current_str = prev + current_str * repeat
        else:
            # regular character
            current_str += ch

    return current_str
