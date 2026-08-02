def brainfuck(code, input_str=''):
    # Tape with 30,000 cells
    tape = [0] * 30000
    ptr = 0
    inp_index = 0
    output_chars = []

    # Precompute bracket matching
    stack = []
    match = {}
    for i, ch in enumerate(code):
        if ch == '[':
            stack.append(i)
        elif ch == ']':
            if not stack:
                raise ValueError('Unmatched closing bracket')
            j = stack.pop()
            match[j] = i
            match[i] = j
    if stack:
        raise ValueError('Unmatched opening bracket')

    i = 0
    n = len(code)
    while i < n:
        cmd = code[i]
        if cmd == '>':
            ptr += 1
            if ptr >= len(tape):
                raise IndexError('Pointer moved beyond tape right bound')
        elif cmd == '<':
            ptr -= 1
            if ptr < 0:
                raise IndexError('Pointer moved before tape start')
        elif cmd == '+':
            tape[ptr] += 1
        elif cmd == '-':
            tape[ptr] -= 1
        elif cmd == '.':
            output_chars.append(chr(tape[ptr]))
        elif cmd == ',':
            if inp_index < len(input_str):
                tape[ptr] = ord(input_str[inp_index])
                inp_index += 1
            else:
                tape[ptr] = 0
        elif cmd == '[':
            if tape[ptr] == 0:
                # jump to matching ]
                i = match[i]
        elif cmd == ']':
            if tape[ptr] != 0:
                # jump back to matching [ (to just after it, so set i to match and loop will i+=1)
                i = match[i]
        # ignore other chars
        i += 1
    return ''.join(output_chars)
