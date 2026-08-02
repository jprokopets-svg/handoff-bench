def decode_string(s: str) -> str:
    """Decode an encoded string with patterns k[encoded_string], supporting nesting.

    Examples:
    - "3[a]2[bc]" -> "aaabcbc"
    - "3[a2[c]]" -> "accaccacc"
    """
    if not s:
        return ""

    num_stack = []  # stack of repeat counts (integers)
    str_stack = []  # stack of previous strings (strings)
    current_num = 0
    current_str = []  # build as list of chars for efficiency

    for ch in s:
        if ch.isdigit():
            # build multi-digit number
            current_num = current_num * 10 + int(ch)
        elif ch == '[':
            # push current context and reset
            str_stack.append(''.join(current_str))
            num_stack.append(current_num)
            current_str = []
            current_num = 0
        elif ch == ']':
            # pop and build repeated string
            repeat = num_stack.pop() if num_stack else 1
            prev = str_stack.pop() if str_stack else ''
            repeated = ''.join(current_str) * repeat
            combined = prev + repeated
            current_str = list(combined)
        else:
            # regular character
            current_str.append(ch)

    # If there are unmatched '[' left (malformed), try to resolve by applying remaining counts
    # This recovers cases like "2[a3[b]" by applying available repeats; if none, just return built string.
    while num_stack and str_stack:
        repeat = num_stack.pop()
        prev = str_stack.pop()
        repeated = ''.join(current_str) * repeat
        current_str = list(prev + repeated)

    return ''.join(current_str)
