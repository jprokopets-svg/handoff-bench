def decode_string(s: str) -> str:
    """
    Decode an encoded string of the form k[encoded_string], where k is a positive integer
    and the content repeats k times. Nesting is allowed.
    
    Examples:
    >>> decode_string('3[a]2[bc]')
    'aaabcbc'
    >>> decode_string('3[a2[c]]')
    'accaccacc'
    >>> decode_string('2[abc]3[cd]ef')
    'abcabccdcdcdef'
    >>> decode_string('abc3[cd]xyz')
    'abccdcdcdxyz'
    >>> decode_string('10[a]')
    'aaaaaaaaaa'
    >>> decode_string('')
    ''
    """
    stack = []
    current_num = 0
    current_str = ''
    
    for char in s:
        if char.isdigit():
            # Build multi-digit numbers
            current_num = current_num * 10 + int(char)
        elif char == '[':
            # Push current state to stack and reset
            stack.append((current_num, current_str))
            current_num = 0
            current_str = ''
        elif char == ']':
            # Pop from stack and build decoded string
            num, prev_str = stack.pop()
            current_str = prev_str + current_str * num
        else:
            # Regular character
            current_str += char
    
    return current_str