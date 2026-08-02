def decode_string(s: str) -> str:
    """Decode encoded strings of the form k[encoded_string] with nesting.

    Examples:
    - decode_string('3[a]2[bc]') -> 'aaabcbc'
    - decode_string('3[a2[c]]') -> 'accaccacc'
    """
    if not s:
        return ''

    count_stack = []
    string_stack = []
    current_num = 0
    current_str = []  # use list for efficiency

    for ch in s:
        if ch.isdigit():
            # build multi-digit number
            current_num = current_num * 10 + int(ch)
        elif ch == '[':
            # push current context
            count_stack.append(current_num)
            string_stack.append(''.join(current_str))
            # reset
            current_num = 0
            current_str = []
        elif ch == ']':
            repeat = count_stack.pop() if count_stack else 1
            prev = string_stack.pop() if string_stack else ''
            current_str = [prev + ''.join(current_str) * repeat]
        else:
            current_str.append(ch)

    return ''.join(current_str)
