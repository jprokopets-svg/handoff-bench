def brainfuck(code, input_str=''):
    """Run a minimal Brainfuck interpreter.

    Tape: 30,000 cells initialized to 0. Data pointer starts at 0.
    Commands: > < + - . , [ ] ; other characters ignored.
    Brackets must be balanced or ValueError is raised.
    """
    # Precompute bracket matches
    stack = []
    jump = {}
    for i, ch in enumerate(code):
        if ch == '[':
            stack.append(i)
        elif ch == ']':
            if not stack:
                raise ValueError('Unmatched ]')
            j = stack.pop()
            jump[j] = i
            jump[i] = j
    if stack:
        raise ValueError('Unmatched [')

    # Tape
    cells = [0] * 30000
    ptr = 0
    ip = 0
    n = len(code)
    input_i = 0
    out_chars = []

    while ip < n:
        cmd = code[ip]
        if cmd == '>':
            ptr += 1
            if ptr >= len(cells):
                # pointer moves beyond tape — typical implementations may extend or error;
                # keep behavior simple and raise IndexError
                raise IndexError('Data pointer moved right out of tape')
            ip += 1
        elif cmd == '<':
            ptr -= 1
            if ptr < 0:
                raise IndexError('Data pointer moved left out of tape')
            ip += 1
        elif cmd == '+':
            cells[ptr] += 1
            ip += 1
        elif cmd == '-':
            cells[ptr] -= 1
            ip += 1
        elif cmd == '.':
            out_chars.append(chr(cells[ptr]))
            ip += 1
        elif cmd == ',':
            if input_i < len(input_str):
                cells[ptr] = ord(input_str[input_i])
                input_i += 1
            else:
                cells[ptr] = 0
            ip += 1
        elif cmd == '[':
            if cells[ptr] == 0:
                # jump to after matching ]
                ip = jump[ip] + 1
            else:
                ip += 1
        elif cmd == ']':
            if cells[ptr] != 0:
                # jump back to just after matching [
                ip = jump[ip] + 1
            else:
                ip += 1
        else:
            # ignore other characters
            ip += 1
    return ''.join(out_chars)
